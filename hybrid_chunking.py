from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer
import spacy
import re

# Load tokenizer and spaCy model
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
nlp = spacy.load("en_core_web_sm")

# 1. Clean and prepare the transcript
def clean_transcript(text):
    text = text.replace('\n', ' ').strip()
    text = re.sub(r'\s+', ' ', text)
    return text

# 2. Use LangChain’s text splitter for initial chunking
def initial_chunking(text, chunk_size=1000, chunk_overlap=150):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_text(text)

# 3. Post-process chunks with tokenizer to ensure token limit
def enforce_token_limit(chunks, max_tokens=512):
    processed_chunks = []
    for chunk in chunks:
        tokens = tokenizer.tokenize(chunk)
        if len(tokens) <= max_tokens:
            processed_chunks.append(chunk)
        else:
            # Slice into subchunks
            subchunk = ""
            current_tokens = 0
            for word in chunk.split():
                word_tokens = tokenizer.tokenize(word)
                if current_tokens + len(word_tokens) > max_tokens:
                    processed_chunks.append(subchunk.strip())
                    subchunk = word + " "
                    current_tokens = len(word_tokens)
                else:
                    subchunk += word + " "
                    current_tokens += len(word_tokens)
            if subchunk:
                processed_chunks.append(subchunk.strip())
    return processed_chunks

# 4. Full Pipeline
def hybrid_chunk_transcript(raw_text):
    cleaned = clean_transcript(raw_text)
    initial_chunks = initial_chunking(cleaned)
    final_chunks = enforce_token_limit(initial_chunks)
    return final_chunks
#text= "When I was first learning to meditate, the instruction was to simply pay attention to my breath and with my mind wandered to bring it back. Sounded simple enough. Yet, I'd sit on these silent retreats, sweating through t-shirts in the middle of winter. I'd take naps every chance I got because it was really hard work. Actually it was exhausting. The instruction was simple enough, but I was missing something really important. So why is it so hard to pay attention? Well studies show that even when we're really trying to pay attention to something, like maybe this talk, at some point about half of us will drift off into a daydream or have this urge to check our Twitter feed. So what's going on here? It turns out that we're fighting one of the most evolutionarily conserved learning processes currently known in science, one that's conserved back to the most basic nervous systems known to man. This reward-based learning process is called positive and negative reinforcement and basically goes like this. We see some food that looks good, our brain says, calories, survival. We eat the food, we taste it, it tastes good, and especially with sugar, our bodies send a signal to our brain that says, remember what you're eating and where you found it. We lay down this context dependent memory and learn to repeat the process next time. See food, eat food, feel good, repeat. Trigger, behavior, reward. Simple right? Well after a while our creative brain say, you know what, you can use this for more than just remembering where food is. Even or next time you feel bad, why don't you try eating something good so you'll feel better? We think our brains are the great idea. Try this and quickly learn that if we eat chocolate or ice cream when we're mad or sad we feel better. Same process, just a different trigger. Instead of this hunger signal coming from our stomach, this emotional signal feeling sad triggers that it's to eat. Maybe in our teenage years we were a nerd at school and we see those rebel kids outside smoking we think, hey I want to be cool so we start smoking. The Marlboro man wasn't adoric and that was no accident. See cool, smoke to be cool, feel good, repeat. Trigger, behavior, reward. And each time we do this we learn to repeat the process and it becomes a habit. So later feeling stressed out triggers that urge to smoke a cigarette or to eat something sweet. Now with these same brain processes we've gone from learning to survive to literally killing ourselves with these habits. Obesity and smoking among the leading preventable causes of morbidity and mortality in the world. So back to my breath, what if instead of fighting our brains or trying to force ourselves to pay attention we instead tapped into this natural reward based learning process but added a twist. What if instead we just got really curious about what was happening in our momentary experience. I'll give you an example. In my lab we studied whether mindfulness training could help people quit smoking. Now just like trying to force myself to pay attention on my breath they could try to force themselves to quit smoking and the majority of them had tried this before and failed on average six times. Now with mindfulness training we dropped a bit about forcing and instead focused on being curious. In fact we even told them to smoke. What? We said go ahead and smoke just be really curious about what is like when you do and what did they notice. Well here's an example from one of our smokers. She said mindful smoking smells like stinky cheese and tastes like chemicals. Yuck! Now she knew cognitively that smoking was bad for her. That's why she joined our program. What she discovered just by being curiously aware when she smoked was that smoking tast"
#print(hybrid_chunk_transcript(text))