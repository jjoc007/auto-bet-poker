from deuces import Deck
from deuces import Card
from deuces import Evaluator
evaluator = Evaluator()

deck = Deck()
board = [Card.new('Th'), Card.new('2d'), Card.new('3d'), Card.new('4d'), Card.new('5d')]
player1_hand = [Card.new('Ac'), Card.new('Kd')]
player2_hand = [Card.new('Ah'), Card.new('Ad')]

Card.print_pretty_cards(board)
Card.print_pretty_cards(player1_hand)
Card.print_pretty_cards(player2_hand)

p1_score = evaluator.evaluate(board, player1_hand)
p2_score = evaluator.evaluate(board, player2_hand)
p1_class = evaluator.get_rank_class(p1_score)
p2_class = evaluator.get_rank_class(p2_score)

print("Player 1 hand rank = %d (%s)" % (p1_score, evaluator.class_to_string(p1_class)))
print("Player 2 hand rank = %d (%s)" % (p2_score, evaluator.class_to_string(p2_class)))

hands = [player1_hand, player2_hand]
evaluator.hand_summary(board, hands)