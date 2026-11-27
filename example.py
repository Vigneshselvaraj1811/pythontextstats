import pythontextstats as textstats

sample_text = "Hello world! This is a sample text to demonstrate text analysis."
result = textstats.analyze(sample_text)

print("Words:", result.word_count)
print("Sentences:", result.sentence_count)
print("Average Word Length:", round(result.average_word_length, 2))
print("Estimated Reading Time (min):", round(result.reading_time, 2))
print("Top Words:", result.word_frequencies)
