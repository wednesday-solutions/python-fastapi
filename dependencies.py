# app/dependencies.py
import pybreaker

# Global Circuit Breaker
circuit_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)
