import math
from scipy.stats import norm


def get_norm_parameters():
    """
    :return: the mean and std estimate of gaussian distribution for transformed features
    """
    loc_hits, scale_hits,loc_log_avg_returned_ob, scale_log_avg_returned_ob,loc_interval_variety_ratio,\
    scale_interval_variety_ratio = 3.691, 1.175,  9.919, 0.532, 0.825, 0.073
    return(loc_hits, scale_hits, loc_log_avg_returned_ob, scale_log_avg_returned_ob, loc_interval_variety_ratio,\
           scale_interval_variety_ratio)


def LogPValue(hits, interval_variety_ratio, avg_returned_ob):
    """
    estimate log likelihood of feature combinations
    :param hits
    :param interval_variety_ratio
    :param avg_returned_ob
    :return: the likelihood of observations
    """
    sqrt_hits = math.sqrt(hits)
    sqrt_interval_variety_ratio = math.sqrt(interval_variety_ratio)
    log_avg_returned_ob = math.log(avg_returned_ob)
    loc_hits, scale_hits,loc_log_avg_returned_ob, scale_log_avg_returned_ob,\
    loc_interval_variety_ratio, scale_interval_variety_ratio = get_norm_parameters()
    p1 = norm.pdf(sqrt_hits, loc_hits, scale_hits)
    p2 = norm.pdf(sqrt_interval_variety_ratio, loc_interval_variety_ratio, scale_interval_variety_ratio)
    p3 = norm.pdf(log_avg_returned_ob, loc_log_avg_returned_ob, scale_log_avg_returned_ob)
    p = [p1, p2, p3]
    try:
        ans = sum([math.log(i) for i in p])
    except:
        ans = -1000
    return(ans)


def IfRobot(hits, interval_variety_ratio, avg_returned_ob):
    """
    check if it's robot based on log likelihood
    :param hits: request count per hour
    :param interval_variety_ratio: the number of unique time intervals between requests over total number of hits
    :param avg_returned_ob: average size of objects returned
    :return: if robot
    """
    threshold = -45
    pvalue = LogPValue(hits, interval_variety_ratio, avg_returned_ob)
    if pvalue < threshold:
        return (True)
    else:
        return (False)


