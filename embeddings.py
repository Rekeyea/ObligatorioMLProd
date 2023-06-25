import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text

def generate_embedding(text: str):
    text_input = tf.keras.layers.Input(shape=(), dtype=tf.string)
    preprocessor = hub.KerasLayer(
        "https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")
    encoder_inputs = preprocessor(text_input)
    encoder = hub.KerasLayer(
        "https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-256_A-4/2",
        trainable=True)
    outputs = encoder(encoder_inputs)
    pooled_output = outputs["pooled_output"]      # [batch_size, 256].
    sequence_output = outputs["sequence_output"]  # [batch_size, seq_length, 256].
    embedding_model = tf.keras.Model(text_input, pooled_output)
    sentences = tf.constant([text])
    result = embedding_model(sentences)
    print(result.numpy())
    return result.numpy().tolist()

