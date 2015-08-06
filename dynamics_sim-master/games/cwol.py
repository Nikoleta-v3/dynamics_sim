from games.game import Game


class CWOL(Game):
    DEFAULT_PARAMS = dict(a=1, b=1, c_low=4, c_high=12, d=-10, w=0.895, p=0.51, player1_prop=0.5)
    PLAYER_LABELS = ('Player 1', 'Player 2')
    STRATEGY_LABELS = (('CWOL', 'CWL', 'C if Low', 'All D'),
                       ('Exit if Look', 'Exit if Defect', 'Exit if defect when low', 'Always Exit'))
    EQUILIBRIA_LABELS = ('CWL', 'CWOL', 'ONLY L', 'All D')

    def __init__(self, a, b, c_low, c_high, d, w, p, player1_prop, equilibrium_tolerance=0.2):
        payoff_matrix_p1 = ((a / (1 - w), a / (1 - w), a / (1 - w), a),
                            (a, a / (1 - w), a / (1 - w), a),
                            (a * p + c_high * (1 - p), (a * p + c_high * (1 - p)) / (1 - p * w), a * p + c_high * (1 - p), a * p + c_high * (1 - p)),
                            (c_low * p + c_high * (1 - p), c_low * p + c_high * (1 - p), (c_low * p + c_high * (1 - p)) / ((1 - w * p)), c_low * p + c_high * (1 - p)))

        payoff_matrix_p2 = ((b / (1 - w), b / (1 - w), b / (1 - w), b),
                            (b, b / (1 - w), b / (1 - w), b),
                            (b * p + d * (1 - p), (b * p + d * (1 - p)) / (1 - p * w), (b * p + d * (1 - p)) / (1 - w), b * p + d * (1 - p)),
                            (d, d, d / ((1 - w * p)), d))

        payoff_matrix = [payoff_matrix_p1, payoff_matrix_p2]
        player_dist = (player1_prop, 1 - player1_prop)
        super(CWOL, self).__init__(payoff_matrices=payoff_matrix, player_frequencies=player_dist, equilibrium_tolerance=equilibrium_tolerance)

    @classmethod
    def classify(cls, params, state, tolerance):
        threshold = 1 - tolerance
        
        if state[0][1] >= threshold:
            return 0#Cooperate with looking
        elif state[0][0] >= threshold:
            return 1#Cooperate with out looking
        elif state[0][2] >= threshold:
            return 2#Only cooperate when low
        elif state[0][3] >= threshold:
            return 3#All D
        else:
            return super(CWOL, cls).classify(params, state, tolerance)
