import textstats

sample_text = "Hello world! This is a sample text to demonstrate text analysis."

print("Words:", textstats.word_count(sample_text))
print("Sentences:", textstats.sentence_count(sample_text))
print("Average Word Length:", round(textstats.average_word_length(sample_text), 2))
print("Estimated Reading Time (min):", round(textstats.reading_time(sample_text), 2))