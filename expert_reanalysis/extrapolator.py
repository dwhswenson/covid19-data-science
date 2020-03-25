import numpy as np

class PercentileExtrapolator:
    """

    Extrapolation works like this: for the ranges where we have an actual probability
    associated, we assume a constant probability density. Outside that range, we assume
    an exponential tail which we determine by fixing the probability density to be
    the same as the last bin (and by requiring normalization).

    Parameters
    ----------
    bins : List[Tuple[Int, Int]]
    probabilities : List[Float]
    """
    def __init__(self, bins, probabilities):
        self.probabilities = probabilities
        self.bins = bins
        self.extra_probability = 1 - sum(self.probabilities)

    def _triangle_rule(self, xval):
        cumulative_prob = 0
        for (bin_min, bin_max), prob in zip(self.bins, self.probabilities):
            if xval > bin_max:
                cumulative_prob += prob
            elif bin_min < xval <= bin_max:
                fraction = (xval - bin_min) / (bin_max - bin_min)
                cumulative_prob += fraction * prob
            else:
                break
        return cumulative_prob

    def _exponential_tail(self, xval):
        bin_min, bin_max = self.bins[-1]
        match_prob_dens = self.probabilities[-1] / (bin_max - bin_min)
        if xval <= bin_max:
            return 0.0

        N = self.extra_probability
        alpha = match_prob_dens / N

        # pdf = lambda x: N * alpha * np.exp(alpha * (x - bin_max))
        return N * (1 - np.exp(-alpha * (xval - bin_max)))

    def invert(self, percentile, resolution=1000):
        # note: an exact version can probably be done, not needing resolution
        xval = 0
        while self(xval) < percentile:
            xval += resolution
        return xval

    def __call__(self, count):
        return self._triangle_rule(count) + self._exponential_tail(count)
