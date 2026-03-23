import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="xyf-competition-mvp", layout="wide")
st.title("xyf-competition-mvp")
st.caption("Streamlit + FastAPI + uv starter")

st.subheader("Quick sanity check")
df = pd.DataFrame({
    "x": np.arange(1, 6),
    "y": np.random.randn(5),
})
st.dataframe(df, use_container_width=True)
st.line_chart(df.set_index("x"))
