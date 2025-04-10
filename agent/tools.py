from typing import Annotated, List, Tuple, Dict, Any
from langchain.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import pandas as pd
import numpy as np
from datetime import datetime

search = DuckDuckGoSearchRun()

@tool
def calculate_roi(
    investment_amount: float,
    yearly_cash_flows: List[float],
    discount_rate: float = 0.1,
    inflation_rate: float = 0.025
) -> Dict[str, Any]:
    """Calculate ROI metrics including NPV, IRR, and payback period.
    
    Args:
        investment_amount: Initial investment amount
        yearly_cash_flows: List of yearly cash flows
        discount_rate: Required rate of return (default 10%)
        inflation_rate: Expected inflation rate (default 2.5%)
    
    Returns:
        Dictionary containing ROI metrics and explanations
    """
    # Calculate NPV
    npv = -investment_amount
    for i, cf in enumerate(yearly_cash_flows):
        npv += cf / ((1 + discount_rate) ** (i + 1))
    
    # Calculate IRR
    cash_flows = [-investment_amount] + yearly_cash_flows
    irr = np.irr(cash_flows)
    
    # Calculate payback period
    cumulative_cf = 0
    payback_period = None
    for i, cf in enumerate(yearly_cash_flows):
        cumulative_cf += cf
        if cumulative_cf >= investment_amount:
            payback_period = i + 1
            break
    
    return {
        "npv": round(npv, 2),
        "irr": round(irr * 100, 2),
        "payback_period": payback_period,
        "metrics_explanation": {
            "npv": "Net Present Value (NPV) shows the present value of future cash flows minus the initial investment. A positive NPV indicates a profitable investment.",
            "irr": "Internal Rate of Return (IRR) is the discount rate that makes the NPV zero. Higher IRR means better investment returns.",
            "payback_period": "Payback period is the time needed to recover the initial investment. Shorter payback period means faster return on investment."
        }
    }

@tool
def search_roi_examples(query: str) -> str:
    """Search for ROI calculation examples and best practices."""
    return search.run(query)

@tool
def calculate_inflation_adjusted_cash_flows(
    base_cash_flow: float,
    years: int,
    inflation_rate: float
) -> List[float]:
    """Calculate inflation-adjusted cash flows for a given number of years."""
    return [base_cash_flow * ((1 + inflation_rate) ** year) for year in range(years)] 