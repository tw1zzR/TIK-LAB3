import numpy as np

def entropy(p):
    p = p[p > 0]
    return -np.sum(p * np.log2(p))

def joint_entropy(p_ab):
    return entropy(p_ab.flatten())

def conditional_entropy(p_ab, p_a):
    h_b_given_a = np.array([entropy(p_ab[i, :] / p_a[i]) if p_a[i] > 0 else 0 for i in range(len(p_a))])
    return np.sum(p_a * h_b_given_a)

def total_conditional_entropy(p_ab):
    p_a = np.sum(p_ab, axis=1)
    p_b = np.sum(p_ab, axis=0)
    h_b_given_a = conditional_entropy(p_ab, p_a)
    h_a_given_b = conditional_entropy(p_ab.T, p_b)
    return h_b_given_a + h_a_given_b

def calculate_entropies(p_ab):
    p_a = np.sum(p_ab, axis=1)
    p_b = np.sum(p_ab, axis=0)

    h_a = entropy(p_a)
    h_b = entropy(p_b)
    h_ab = joint_entropy(p_ab)
    h_b_given_a = conditional_entropy(p_ab, p_a)
    h_a_given_b = conditional_entropy(p_ab.T, p_b)
    total_h = total_conditional_entropy(p_ab)

    return {
        "H(A)": h_a,
        "H(B)": h_b,
        "H(A, B)": h_ab,
        "H(B | A)": h_b_given_a,
        "H(A | B)": h_a_given_b,
        "H(B | A) + H(A | B)": total_h
    }