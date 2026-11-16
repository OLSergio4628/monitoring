"""Cálculo sencillo de PSI para detectar cambio entre referencia y producción."""
import numpy as np

def population_stability_index(reference, current, bins=10, eps=1e-6):
    reference=np.asarray(reference, dtype=float)
    current=np.asarray(current, dtype=float)
    edges=np.unique(np.quantile(reference, np.linspace(0,1,bins+1)))
    if len(edges)<3:
        return 0.0
    edges[0], edges[-1] = -np.inf, np.inf
    r,_=np.histogram(reference,bins=edges)
    c,_=np.histogram(current,bins=edges)
    rp=np.clip(r/r.sum(),eps,None); cp=np.clip(c/c.sum(),eps,None)
    return float(np.sum((cp-rp)*np.log(cp/rp)))

if __name__ == "__main__":
    rng=np.random.default_rng(7)
    ref=rng.normal(0,1,5000)
    prod=rng.normal(0.8,1.2,5000)  # cambio simulado
    psi=population_stability_index(ref,prod)
    print(f"PSI={psi:.4f}")
