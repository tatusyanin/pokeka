# deck/views.py
from django.shortcuts import render, redirect
from .models import Deck, Card
from .forms import DeckForm, CardForm

# デッキ一覧・登録
def deck_list(request):
    decks = Deck.objects.all()
    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('deck_list')
    else:
        form = DeckForm()

    return render(request, 'deck/deck_list.html', {'decks': decks, 'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
import random

def deck_detail(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    cards = deck.cards.all()
    total_count = sum(card.count for card in cards)
    over_limit = total_count > 60

    if request.method == 'POST':
        # 新しいカードの登録
        name = request.POST.get('name')
        count = int(request.POST.get('count', 1))
        is_key_card = request.POST.get('is_key_card') == 'on'
        key_card_count = int(request.POST.get('key_card_count', 0))
        
        if name and count > 0:
            card = Card.objects.create(
                deck=deck,
                name=name,
                count=count,
                is_key_card=is_key_card,
                key_card_count=key_card_count
            )
            card.save()
        
        return redirect('deck_detail', pk=pk)

    # サイドカードランダム配置 (6枚をランダムに選ぶ)
    all_cards = []
    for card in cards:
        all_cards.extend([card] * card.count)
    if len(all_cards) >= 6:
        side_cards = random.sample(all_cards, 6)
    else:
        side_cards = all_cards  # すべてのカードをそのまま使う
    # キーカード判定
    key_cards = [card for card in cards if card.is_key_card]
    side_key_cards = [card for card in side_cards if card.is_key_card]
    key_cards_in_side = len(side_key_cards)

    # サイド落ち確率計算
    side_drop_rate = round((key_cards_in_side / len(key_cards)) * 100, 2) if key_cards else 0
    # 戦略アドバイス
    if side_drop_rate > 50:
        advice = "キーカードがサイドに多く落ちています。慎重に立ち回りましょう。"
    else:
        advice = "キーカードは手札に多くあります。積極的に攻めましょう。"

    # カテゴリ別の枚数を集計
    category_counts = {
        'ポケモン': cards.filter(category='ポケモン').aggregate(Sum('count'))['count__sum'] or 0,
        'グッズ': cards.filter(category='グッズ').aggregate(Sum('count'))['count__sum'] or 0,
        'サポート': cards.filter(category='サポート').aggregate(Sum('count'))['count__sum'] or 0,
        'ポケモンのどうぐ': cards.filter(category='ポケモンのどうぐ').aggregate(Sum('count'))['count__sum'] or 0,
        'スタジアム': cards.filter(category='スタジアム').aggregate(Sum('count'))['count__sum'] or 0,
        'エネルギー': cards.filter(category='エネルギー').aggregate(Sum('count'))['count__sum'] or 0,
    }
    
    # データをテンプレートに渡す
    context = {
        'deck': deck,
        'cards': cards,
        'side_cards': side_cards,
        'side_drop_rate': side_drop_rate,
        'advice': advice,
        'key_cards': key_cards,
        'category_counts': category_counts,
        'total_count': total_count,  # 総枚数をテンプレートに渡す
        'over_limit': over_limit,  # 警告フラグをテンプレートに渡す
    }

    return render(request, 'deck/deck_detail.html', context)
        

def home(request):
    return render(request, 'deck/home.html')

def add_card(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    print(deck)
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            # フォームからカードを取得
            card = form.save(commit=False)
            card.deck = deck  # カードを現在のデッキに紐付ける
            card.save()  # 保存


            # 重要カードの処理
            if card.is_key_card:
                card.key_card_count = form.cleaned_data.get('key_card_count', 0)  # 辞書型の .get() を正しく使用

            card.save()  # カードを保存

            return redirect('deck_detail', pk=deck.pk)  # 追加後にデッキ詳細にリダイレクト
    else:
        form = CardForm()
    return render(request, 'deck/add_card.html', {'deck': deck, 'form': form})

def delete_card(request, deck_pk, card_pk):
    deck = get_object_or_404(Deck, pk=deck_pk)
    card = get_object_or_404(Card, pk=card_pk, deck=deck)
    
    if request.method == 'POST':
        card.delete()
        return redirect('deck_detail', pk=deck.pk)
    
    return render(request, 'deck/delete_card.html', {'deck': deck, 'card': card})
from .forms import CardEditForm


def edit_card(request, deck_pk, card_pk):
    deck = get_object_or_404(Deck, pk=deck_pk)
    card = get_object_or_404(Card, pk=card_pk, deck=deck)
    
    if request.method == 'POST':
        form = CardEditForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect('deck_detail', pk=deck.pk)
    else:
        form = CardEditForm(instance=card)
    
    return render(request, 'deck/edit_card.html', {'form': form, 'deck': deck, 'card': card})


def deck_delete(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    
    if request.method == 'POST':
        deck.delete()
        return redirect('deck_list')  # 削除後にデッキ一覧にリダイレクト

    return render(request, 'deck/deck_confirm_delete.html', {'deck': deck})


def edit_deck(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    
    if request.method == 'POST':
        form = DeckForm(request.POST, instance=deck)
        if form.is_valid():
            form.save()
            return redirect('deck_list')
    else:
        form = DeckForm(instance=deck)
    
    return render(request, 'deck/edit_deck.html', {'form': form, 'deck': deck})



# サイドカードランダム配置を行う新しいビュー
def random_side_cards(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    cards = deck.cards.all()

    # サイドカードランダム配置 (6枚をランダムに選ぶ)
    all_cards = []
    for card in cards:
        all_cards.extend([card] * card.count)
    side_cards = random.sample(all_cards, 6)

    # キーカード判定
    key_cards = [card for card in cards if card.is_key_card]
    side_key_cards = [card for card in side_cards if card.is_key_card]
    key_cards_in_side = len(side_key_cards)

    # サイド落ち確率計算
    side_drop_rate = round((key_cards_in_side / len(key_cards)) * 100, 2) if key_cards else 0
    # 戦略アドバイス
    if side_drop_rate > 50:
        advice = "キーカードがサイドに多く落ちています。慎重に立ち回りましょう。"
    else:
        advice = "キーカードは手札に多くあります。積極的に攻めましょう。"

    # サイドカードをテンプレートに渡す
    context = {
        'deck': deck,
        'side_cards': side_cards,
        'side_drop_rate': side_drop_rate,
        'advice': advice,
        'key_cards': key_cards,
    }

    return render(request, 'deck/random_side_cards.html', context)

def create_deck(request):
    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = form.save()
            return redirect('add_card', pk=deck.pk)  # 作成後にカード追加ページへ
    else:
        form = DeckForm()
    
    return render(request, 'deck/create_deck.html', {'form': form})



from .forms import AddCardForm  # フォームを作成する
all_cards = []

from .forms import AddCardForm
import random

# カードをデッキに追加するビュー
def add_card_to_deck(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    all_cards = []

    # デッキのカードをリストに追加
    for card in deck.cards.all():
        all_cards.extend([card] * card.count)

    # デッキのカード数が60枚の場合のみ、ランダムに6枚を選ぶ
    if len(all_cards) == 60:
        side_cards = random.sample(all_cards, 6)  # 6枚をランダムに抽出
    else:
        side_cards = []  # それ以外の場合は空のリスト

    # もしデッキのカード数が60枚未満の場合は、カード追加ページにリダイレクト
    if len(all_cards) < 60:
        return redirect('add_card_page', pk=pk)

    print(side_cards)

    if request.method == "POST":
        form = AddCardForm(request.POST)
        if form.is_valid():
            card = form.cleaned_data['card']  # フォームからカードを取得
            deck.cards.add(card)  # デッキにカードを追加
            return redirect('deck_detail', pk=pk)  # デッキ詳細ページにリダイレクト
    else:
        form = AddCardForm()

    return render(request, 'deck/add_card.html', {'form': form, 'deck': deck, 'side_cards': side_cards})

def game_simulation(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    cards = list(deck.cards.all())

    hand = []
    side_cards = []
    mulligan_count = 0

    # マリガン処理
    while True:
        hand = random.sample(cards, 7)  # 7枚引く
        has_basic = any(card.category == 'たねポケモン' for card in hand)
        if has_basic:
            break
        mulligan_count += 1  # マリガン回数を記録

    # サイドカード6枚を配置
    side_cards = random.sample([card for card in cards if card not in hand], 6)

    # 重要カードのサイド落ちチェック
    key_cards_in_side = [card for card in side_cards if card.is_key_card]
    key_card_warning = len(key_cards_in_side) >= 7 and len([c for c in cards if c.is_key_card]) >= 10

    return render(request, 'deck/game_simulation.html', {
        'deck': deck,
        'hand': hand,
        'side_cards': side_cards,
        'mulligan_count': mulligan_count,
        'key_card_warning': key_card_warning,
    })


# from .models import Deck, Card, MulliganResult

# import matplotlib.pyplot as plt
# from io import BytesIO
# import base64

# def mulligan_simulation(request, pk):
#     deck = get_object_or_404(Deck, pk=pk)
#     cards = list(deck.cards.all())
#     total_trials = 100
#     total_mulligans = 0
#     mulligan_counts = []

#     for _ in range(total_trials):
#         mulligan = True
#         count = 0
#         while mulligan:
#             hand = random.sample(cards, 7)
#             has_basic = any(card.category == 'たねポケモン' for card in hand)
#             if has_basic:
#                 mulligan = False
#             else:
#                 count += 1
#         total_mulligans += count
#         mulligan_counts.append(count)

#     mulligan_rate = (total_mulligans / total_trials) * 100

#     # サイドカードの配置
#     side_cards = deck.draw_side_cards()
#     key_cards_in_side = [card for card in side_cards if card.is_key_card]

#     # 統計データの可視化 (ヒストグラム)
#     # plt.hist(mulligan_counts, bins=range(max(mulligan_counts) + 2), alpha=0.7, color='blue', edgecolor='black')
#     # plt.xlabel('マリガン回数')
#     # plt.ylabel('頻度')
#     # plt.title('マリガン回数の分布')
    
#     # グラフを画像として保存
#     # buffer = BytesIO()
#     # plt.savefig(buffer, format='png')
#     # buffer.seek(0)
#     # image_png = buffer.getvalue()
#     # buffer.close()
#     # graph_base64 = base64.b64encode(image_png).decode('utf-8')

#     return render(request, 'deck/mulligan_result.html', {
#         'deck': deck,
#         'total_trials': total_trials,
#         'total_mulligans': total_mulligans,
#         'mulligan_rate': round(mulligan_rate, 2),
#         'side_cards': side_cards,
#         'key_cards_in_side': key_cards_in_side,
#         # 'graph_base64': graph_base64,
#     })


# def simulation_setup(request, pk):
#     deck = get_object_or_404(Deck, pk=pk)
#     cards = list(Card.objects.filter(deck=deck).values('name', 'count', 'category'))

#     # デッキ構築
#     deck_list = []
#     for card in cards:
#         deck_list.extend([card['name']] * card['count'])
#     random.shuffle(deck_list)
#     hand = deck_list[:7]

#     # シミュレーション
#     total_trials = 100
#     total_mulligans = 0
#     mulligan_counts = []

#     for _ in range(total_trials):
#         hand = []
#         mulligan_count = 0

#         while True:
#             # 7枚引く
#             hand = random.sample(deck_list, 7)

#             # たねポケモンの確認
#             basic_pokemon = [card for card in hand if "たね" in card]  # 例: カード名に「たね」を含む

#             if basic_pokemon:
#                 break
#             else:
#                 mulligan_count += 1
#                 total_mulligans += 1
        
#         mulligan_counts.append(mulligan_count)

#     # 統計データ
#     mulligan_rate = (total_mulligans / total_trials) * 100

#     # ヒストグラムの作成
#     # plt.hist(mulligan_counts, bins=range(max(mulligan_counts)+2), alpha=0.75, edgecolor='black')
#     # plt.xlabel('マリガン回数')
#     # plt.ylabel('試行回数')
#     # plt.title('マリガン回数の分布')
#     # plt.grid(True)
#     # import io

#     # # グラフを画像としてエンコード
#     # buf = io.BytesIO()
#     # plt.savefig(buf, format='png')
#     # buf.seek(0)
#     # graph_base64 = base64.b64encode(buf.read()).decode('utf-8')
#     # plt.close()

#     context = {
#         'deck': deck,
#         'total_trials': total_trials,
#         'total_mulligans': total_mulligans,
#         'mulligan_rate': round(mulligan_rate, 2),
#         # 'graph_base64': graph_base64
#     }
#     return render(request, 'deck/simulation_setup.html', context)