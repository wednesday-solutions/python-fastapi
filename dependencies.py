# app/dependencies.py
from __future__ import annotations

import pybreaker

# Global Circuit Breaker
circuit_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)
