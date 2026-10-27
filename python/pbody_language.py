"""
P-Body Language Processing (Broca's Area)
Phase 4: Narrow language model with token representation, word prediction, and context
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import time


class Vocabulary:
    """Simple vocabulary encoder for narrow language model"""
    
    def __init__(self, max_size: int = 1000):
        self.word_to_id: Dict[str, int] = {}
        self.id_to_word: Dict[int, str] = {}
        self.word_frequency: Dict[str, int] = defaultdict(int)
        self.max_size = max_size
        self.next_id = 0
        
        # Add basic tokens
        self._add_token("<UNK>")  # Unknown
        self._add_token("<PAD>")  # Padding
        self._add_token("<START>")  # Start of sequence
        self._add_token("<END>")  # End of sequence
    
    def _add_token(self, token: str):
        """Add a token to vocabulary"""
        if token not in self.word_to_id:
            self.word_to_id[token] = self.next_id
            self.id_to_word[self.next_id] = token
            self.next_id += 1
    
    def add_word(self, word: str) -> int:
        """Add word to vocabulary, return its ID"""
        if word in self.word_to_id:
            self.word_frequency[word] += 1
            return self.word_to_id[word]
        
        if len(self.word_to_id) >= self.max_size:
            return self.word_to_id["<UNK>"]
        
        self.word_to_id[word] = self.next_id
        self.id_to_word[self.next_id] = word
        self.word_frequency[word] = 1
        word_id = self.next_id
        self.next_id += 1
        
        return word_id
    
    def encode(self, text: str) -> List[int]:
        """Encode text to token IDs"""
        words = text.lower().split()
        ids = []
        for word in words:
            # Strip punctuation
            word = word.strip(".,!?;:\"'()[]{}")
            if word:
                word_id = self.word_to_id.get(word, self.word_to_id["<UNK>"])
                ids.append(word_id)
                self.add_word(word)  # Add if new
        return ids
    
    def decode(self, ids: List[int]) -> str:
        """Decode token IDs to text"""
        words = []
        for id in ids:
            if id in self.id_to_word:
                word = self.id_to_word[id]
                if word not in ["<PAD>", "<START>", "<END>"]:
                    words.append(word)
        return " ".join(words)
    
    def get_size(self) -> int:
        """Get vocabulary size"""
        return len(self.word_to_id)


class ContextWindow:
    """Maintains current context (what P-Body is thinking about)"""
    
    def __init__(self, size: int = 5):
        self.size = size
        self.tokens: List[int] = []
        self.emotion_tags: List[str] = []
        self.timestamp: float = time.time()
    
    def add(self, token_id: int, emotion: str = "neutral"):
        """Add token to context"""
        self.tokens.append(token_id)
        self.emotion_tags.append(emotion)
        
        # Keep only recent context
        if len(self.tokens) > self.size:
            self.tokens.pop(0)
            self.emotion_tags.pop(0)
        
        self.timestamp = time.time()
    
    def get_context(self) -> List[int]:
        """Get current context tokens"""
        return self.tokens.copy()
    
    def get_emotion_context(self) -> str:
        """Get dominant emotion in context"""
        if not self.emotion_tags:
            return "neutral"
        
        # Most recent emotion
        return self.emotion_tags[-1]
    
    def clear(self):
        """Clear context"""
        self.tokens.clear()
        self.emotion_tags.clear()
    
    def is_empty(self) -> bool:
        """Check if context is empty"""
        return len(self.tokens) == 0


class WordPredictor:
    """Predicts next word based on context"""
    
    def __init__(self, vocab_size: int = 100):
        self.vocab_size = vocab_size
        
        # Transition probabilities: context → next word probabilities
        # Simplified: uses n-gram style predictions
        self.unigram_probs: np.ndarray = np.ones(vocab_size) / vocab_size
        self.bigram_probs: Dict[int, np.ndarray] = {}
        self.trigram_probs: Dict[Tuple[int, int], np.ndarray] = {}
        
        # Learning rate
        self.learning_rate = 0.1
    
    def update(self, context: List[int], next_word: int):
        """Update prediction model with new observation"""
        # Update unigram
        self.unigram_probs[next_word] += self.learning_rate
        self.unigram_probs /= self.unigram_probs.sum()
        
        # Update bigram
        if context:
            prev_word = context[-1]
            if prev_word not in self.bigram_probs:
                self.bigram_probs[prev_word] = np.ones(self.vocab_size) / self.vocab_size
            
            self.bigram_probs[prev_word][next_word] += self.learning_rate
            self.bigram_probs[prev_word] /= self.bigram_probs[prev_word].sum()
        
        # Update trigram
        if len(context) >= 2:
            bigram = (context[-2], context[-1])
            if bigram not in self.trigram_probs:
                self.trigram_probs[bigram] = np.ones(self.vocab_size) / self.vocab_size
            
            self.trigram_probs[bigram][next_word] += self.learning_rate
            self.trigram_probs[bigram] /= self.trigram_probs[bigram].sum()
    
    def predict(self, context: List[int], top_k: int = 5) -> List[Tuple[int, float]]:
        """Predict next word, return top-k predictions with probabilities"""
        if not context:
            # Use unigram
            probs = self.unigram_probs.copy()
        elif len(context) == 1 and context[-1] in self.bigram_probs:
            # Use bigram
            probs = self.bigram_probs[context[-1]].copy()
        elif len(context) >= 2:
            # Use trigram if available
            bigram = (context[-2], context[-1])
            if bigram in self.trigram_probs:
                probs = self.trigram_probs[bigram].copy()
            elif context[-1] in self.bigram_probs:
                probs = self.bigram_probs[context[-1]].copy()
            else:
                probs = self.unigram_probs.copy()
        else:
            probs = self.unigram_probs.copy()
        
        # Suppress special tokens
        probs[0] *= 0.1  # <UNK>
        probs[1] *= 0.0  # <PAD>
        probs[2] *= 0.0  # <START>
        probs[3] *= 0.0  # <END>
        
        # Normalize
        total = probs.sum()
        if total > 0:
            probs /= total
        
        # Get top-k predictions
        top_indices = np.argsort(probs)[-top_k:][::-1]
        predictions = [(idx, probs[idx]) for idx in top_indices]
        
        return predictions
    
    def get_prediction_accuracy(self, context: List[int], actual: int) -> float:
        """Check if prediction was correct (for dopamine reward)"""
        predictions = self.predict(context, top_k=1)
        if predictions and predictions[0][0] == actual:
            return 1.0
        return 0.0


class BrocasArea:
    """
    Language processing center
    Handles tokenization, prediction, and generation
    """
    
    def __init__(self, max_vocab: int = 1000, context_size: int = 5):
        self.vocab = Vocabulary(max_size=max_vocab)
        self.context = ContextWindow(size=context_size)
        self.predictor = WordPredictor(vocab_size=max_vocab)
        
        # Processing stats
        self.total_processed = 0
        self.total_predictions = 0
        self.correct_predictions = 0
        
        # Language activity (for brain integration)
        self.activity_level = 0.0
    
    def process_input(self, text: str, emotion: str = "neutral") -> dict:
        """Process language input"""
        # Encode to tokens
        token_ids = self.vocab.encode(text)
        
        if not token_ids:
            return {"processed": False, "reason": "No valid tokens"}
        
        # Update context
        for token_id in token_ids:
            self.context.add(token_id, emotion)
            
            # Update predictor (learning)
            if len(self.context.tokens) > 1:
                context = self.context.tokens[:-1]
                self.predictor.update(context, token_id)
        
        self.total_processed += len(token_ids)
        self.activity_level = min(1.0, len(token_ids) / 10.0)
        
        return {
            "processed": True,
            "tokens": token_ids,
            "token_count": len(token_ids),
            "context_size": len(self.context.tokens),
            "vocab_size": self.vocab.get_size(),
        }
    
    def predict_next(self, top_k: int = 5) -> List[Tuple[str, float]]:
        """Predict next word(s)"""
        if self.context.is_empty():
            return []
        
        context = self.context.get_context()
        predictions = self.predictor.predict(context, top_k=top_k)
        
        # Convert to words
        word_predictions = []
        for token_id, prob in predictions:
            word = self.vocab.id_to_word.get(token_id, "<UNK>")
            word_predictions.append((word, prob))
        
        self.total_predictions += 1
        
        return word_predictions
    
    def generate_response(self, max_length: int = 10) -> str:
        """Generate a response based on context"""
        if self.context.is_empty():
            return ""
        
        generated = []
        context = self.context.get_context()
        
        for _ in range(max_length):
            # Predict next word
            predictions = self.predictor.predict(context, top_k=3)
            
            if not predictions:
                break
            
            # Sample from top predictions (weighted)
            token_ids = [p[0] for p in predictions]
            probs = np.array([p[1] for p in predictions])
            probs /= probs.sum()
            
            # Choose word
            chosen_idx = np.random.choice(len(token_ids), p=probs)
            chosen_token = token_ids[chosen_idx]
            
            # Check for end token
            word = self.vocab.id_to_word.get(chosen_token, "")
            if word in ["<END>", "<PAD>"]:
                break
            
            generated.append(chosen_token)
            context.append(chosen_token)
            
            # Keep context window size
            if len(context) > self.context.size:
                context.pop(0)
        
        # Decode to text
        return self.vocab.decode(generated)
    
    def get_prediction_accuracy(self) -> float:
        """Get overall prediction accuracy"""
        if self.total_predictions == 0:
            return 0.0
        return self.correct_predictions / self.total_predictions
    
    def get_state(self) -> dict:
        """Get language processing state"""
        return {
            "vocab_size": self.vocab.get_size(),
            "context_size": len(self.context.tokens),
            "context_emotion": self.context.get_emotion_context(),
            "total_processed": self.total_processed,
            "total_predictions": self.total_predictions,
            "activity_level": self.activity_level,
            "top_words": self._get_top_words(),
        }
    
    def _get_top_words(self) -> List[str]:
        """Get most frequent words"""
        sorted_words = sorted(
            self.vocab.word_frequency.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [word for word, _ in sorted_words[:10]]
    
    def clear_context(self):
        """Clear context (e.g., during sleep)"""
        self.context.clear()
        self.activity_level = 0.0