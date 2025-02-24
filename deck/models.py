from django.db import models

# デッキモデル
from django.db import models
import random

# デッキモデル
class Deck(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # def draw_hand(self):
    #     """デッキから7枚の手札を引く"""
    #     all_cards = list(self.cards.all())
    #     deck_list = [card for card in all_cards for _ in range(card.count)]
    #     random.shuffle(deck_list)
    #     return deck_list[:7]

    # def has_basic_pokemon(self, hand):
    #     """手札にたねポケモンがいるか確認"""
    #     return any(card.category == 'たねポケモン' for card in hand)

    # def simulate_mulligan(self):
    #     """マリガンシミュレーション"""
    #     mulligan_count = 0
    #     hand = self.draw_hand()
            
    #     while not self.has_basic_pokemon(hand):
    #         mulligan_count += 1
    #         hand = self.draw_hand()
            
    #     return hand, mulligan_count

    # def draw_side_cards(self):
    #     """サイドカード6枚をランダムに選択"""
    #     all_cards = list(self.cards.all())
    #     deck_list = [card for card in all_cards for _ in range(card.count)]
    #     random.shuffle(deck_list)
    #     return deck_list[:6]

# カードモデル
class Card(models.Model):
    CATEGORY_CHOICES = [
        ('ポケモン', 'ポケモン'),
        ('たねポケモン', 'たねポケモン'),
        ('グッズ', 'グッズ'),
        ('サポート', 'サポート'),
        ('ポケモンのどうぐ', 'ポケモンのどうぐ'),
        ('スタジアム', 'スタジアム'),
        ('エネルギー', 'エネルギー'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    count = models.PositiveIntegerField(default=1)  # デッキに登録している枚数
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name="cards")
    is_key_card = models.BooleanField(default=False)  # 重要カードかどうか
    key_card_count = models.PositiveIntegerField(default=0)  # 重要カード枚数

    def __str__(self):
        return f"{self.name} ({self.count}枚)"

# # マリガン結果モデル
# class MulliganResult(models.Model):
#     deck = models.ForeignKey('Deck', on_delete=models.CASCADE)
#     total_trials = models.IntegerField(default=0)
#     total_mulligans = models.IntegerField(default=0)
#     mulligan_rate = models.FloatField(default=0.0)
#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.deck.name} - マリガン率: {self.mulligan_rate}%"
    
    