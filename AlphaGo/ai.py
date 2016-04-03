"""Policy players"""
import numpy as np


class GreedyPolicyPlayer(object):
	"""A CNN player that uses a greedy policy (i.e. chooses the highest probability
	   move at each point)
	"""
	def __init__(self, policy_function):
		self.policy = policy_function

	def get_move(self, state):
		action_probs = self.policy.eval_state(state)
		if len(action_probs) > 0:
			sensible_actions = [a for a in action_probs if not state.is_eye(
				a[0], state.current_player)]
			if len(sensible_actions) > 0:
				max_prob = max(sensible_actions, key=lambda (a, p): p)
				return max_prob[0]
			else:
				# No legal moves available, so do pass move
				return None
		else:
			# No legal moves available, so do pass move
			return None

	def copy(self):
		return GreedyPolicyPlayer(self.policy)


class ProbabilisticPolicyPlayer(object):
	"""A CNN player that uses a probabilistic policy (i.e. with high probability,
	   chooses one of the best moves at each point)
	"""
	def __init__(self, policy_function):
		self.policy = policy_function

	def get_move(self, state):
		action_probs = self.policy.eval_state(state)
		if len(action_probs) > 0:
			sensible_actions = [a for a in action_probs if not state.is_eye(
				a[0], state.current_player)]
			if len(sensible_actions) > 0:
				probs = [s[1] for s in sensible_actions]
				probs = np.array(probs) / np.sum(probs)  # Normalize
				ichoice = np.random.choice(len(probs), p=probs)
				return sensible_actions[ichoice][0]
			else:
				# No legal moves available, so do pass move
				return None
		else:
			# No legal moves available, so do pass move
			return None

	def copy(self):
		return ProbabilisticPolicyPlayer(self.policy)
