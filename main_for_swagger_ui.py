from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math

app = FastAPI(title="Arithmetic API", description="Perform math operations", version="1.0.0")

class Expression(BaseModel):
    expression: str

class Value(BaseModel):
    value: float

class PowerInput(BaseModel):
    base: float
    exponent: float

@app.post("/calculate")
async def calculate(expr: Expression):
    try:
        result = eval(expr.expression)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/square_root")
async def square_root(val: Value):
    try:
        return {"result": math.sqrt(val.value)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/power")
async def power(vals: PowerInput):
    try:
        return {"result": vals.base ** vals.exponent}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
