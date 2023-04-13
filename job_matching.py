import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
sys.path.append('.')
#from gensim.models import Word2Vec
#from gensim.models.fasttext import FastText
#from keras.preprocessing.text import Tokenizer
#from tensorflow.keras.preprocessing.sequence import pad_sequences
#from keras.layers import Input, Embedding, LSTM, Dense, Lambda
#from keras.models import Model
#from keras import backend as K
#import gensim.downloader as api

class JobMatching:
    def __init__(self):
        self.jobs = self.load_jobs()

    
    def load_resume(self):
        resume = open("data/Resume-Iqra-2023.txt").read()
        return resume
    
    def load_jobs(self):
        jobs = pd.read_csv("data/dataworld-jobs-sample.csv")
        jobs.dropna(subset=['Job Description'], inplace=True)
        jobs.fillna('', inplace=True)
        jobs = jobs.rename(columns={'Job Title': 'JobTitle', 'Job Description': 'JobDescription', 'Job Type':'JobType'})
        return jobs
    
    def get_all_jobs(self):
        jobs = self.jobs
        jobs = jobs[['JobTitle', 'JobDescription', 'JobType', 'Categories',
       'Location', 'City', 'State', 'Country', 'Zip Code', 'Address',
       'Salary From', 'Salary To', 'Salary Period', 'Apply Url', 'Apply Email',
       'Employees', 'Industry', 'Company Name', 'Employer Email',
       'Employer Website', 'Employer Phone', 'Employer Logo',
       'Companydescription', 'Employer Location', 'Uniq Id',
       'Crawl Timestamp']]
        return jobs.head(20).to_dict(orient='records')
    
    def keyword_matching(self,resume,jobs):
        vectorizer = CountVectorizer()
        keywords = vectorizer.fit_transform([resume]).toarray()[0]

        keywords_match = []
        for i in range(len(jobs)):
            job_description_keywords = vectorizer.transform([jobs['JobDescription'].iloc[i]]).toarray()[0]
            job_requirement_keywords = vectorizer.transform([jobs['JobRequirment'].iloc[i]]).toarray()[0]
            match = all(job_description_keywords[i] >= keywords[i] or job_requirement_keywords[i] >= keywords[i] for i in range(len(keywords)))
            keywords_match.append(match)

        # Add keywords_match column to books dataframe
        jobs['keywords_match'] = keywords_match
        

    '''def siamese_similarity(self, text1, text2):
        # Tokenize the texts
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts([text1, text2])

        # Convert the texts to sequences of indices
        seq1 = tokenizer.texts_to_sequences([text1])[0]
        seq2 = tokenizer.texts_to_sequences([text2])[0]

        # Pad the sequences to a fixed length
        max_len = 20
        padded_seq1 = pad_sequences([seq1], maxlen=max_len, padding='post', truncating='post')[0]
        padded_seq2 = pad_sequences([seq2], maxlen=max_len, padding='post', truncating='post')[0]

        # Load the pre-trained FastText model
        #model = FastText.load_fasttext_format('cc.en.300.bin')
        model = api.load('fasttext-wiki-news-subwords-300')

        # Encode the sequences using the FastText model
        embedding_matrix = np.zeros((len(tokenizer.word_index) + 1, model.vector_size))
        for word, i in tokenizer.word_index.items():
            if word in model:
                embedding_matrix[i] = model[word]

        left_input = Input(shape=(max_len,))
        right_input = Input(shape=(max_len,))

        embedding_layer = Embedding(input_dim=len(tokenizer.word_index) + 1,
                                    output_dim=model.vector_size,
                                    weights=[embedding_matrix],
                                    input_length=max_len,
                                    trainable=False)

        left_embedded = embedding_layer(left_input)
        right_embedded = embedding_layer(right_input)

        lstm_units = 64
        lstm_layer = LSTM(lstm_units)

        left_lstm = lstm_layer(left_embedded)
        right_lstm = lstm_layer(right_embedded)

        # Define the similarity function (in this case, cosine similarity)
        def cosine_similarity(x):
            left, right = x
            dot_product = left * right
            dot_product = K.sum(dot_product, axis=1, keepdims=True)
            left_norm = K.sqrt(K.sum(K.square(left), axis=1, keepdims=True))
            right_norm = K.sqrt(K.sum(K.square(right), axis=1, keepdims=True))
            return dot_product / (left_norm * right_norm)

        similarity_layer = Lambda(cosine_similarity)

        similarity = similarity_layer([left_lstm, right_lstm])

        siamese_model = Model(inputs=[left_input, right_input], outputs=similarity)

        siamese_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Predict the similarity between the two texts
        similarity_score = siamese_model.predict([padded_seq1.reshape(1, -1), padded_seq2.reshape(1, -1)])[0][0]
        return similarity_score

    
    def siamese_scores(self,resume,jobs):
        similarity_scores = []
        for i in range(len(jobs)):
            similarity = self.siamese_similarity(resume, jobs['JobDescription'].iloc[i])
            similarity_scores.append(similarity)
            
        jobs['siamese_similarity'] = similarity_scores
        jobs = jobs.sort_values('siamese_similarity', ascending=False)'''
            
    def cosine_similarity(self,resume,jobs):
        vectorizer = TfidfVectorizer()
        resume_vector = vectorizer.fit_transform([resume])

        similarity_scores = []
        for i in range(len(jobs)):
            job_vector = vectorizer.transform([jobs['JobDescription'].iloc[i]])
            similarity = cosine_similarity(resume_vector, job_vector)[0][0]
            similarity_scores.append(similarity)
            
        jobs['cosine_similarity'] = similarity_scores
        
    def get_jobs_matched(self,resume):
        jobs = self.jobs
        self.cosine_similarity(resume,jobs)
        #self.siamese_scores(resume,jobs)
        jobs = jobs.sort_values(by=['cosine_similarity'], ascending=False)
        #jobs = jobs[['date','Title','Company','Eligibility','Location','JobDescription','JobRequirment','RequiredQual','ApplicationP']]
        return jobs.head(20).to_dict(orient='records')
        
if __name__ == '__main__':
    job_matching = JobMatching()
    resume = job_matching.load_resume()
    results = job_matching.get_jobs_matched(resume)
    print(results)
    

        