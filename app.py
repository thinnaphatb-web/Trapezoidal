import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Trapezoidal Rule App")
st.title("Numerical Integration")
st.header("การประมาณค่าอินทิกรัลด้วย Trapezoidal Rule")
st.write("แอปพลิเคชันนี้จำลองการหาพื้นที่ใต้กราฟของฟังก์ชัน $f(x) = x^2 + 1$")

with st.sidebar:
    st.header("Parameters")
    a = st.number_input("Lower bound (a)", value=0.0, step=1.0)
    b = st.number_input("Upper bound (b)", value=5.0, step=1.0)
    n = st.slider("Number of subintervals (n)", min_value=1, max_value=50, value=10)
    show_table = st.checkbox("Show data table", value=True)

if a >= b:
    st.warning("กรุณากำหนดค่าขอบเขตล่าง (a) ให้น้อยกว่าขอบเขตบน (b)")
    st.stop()

def f(x):
    return x**2 + 1

x_smooth = np.linspace(a, b, 200)
y_smooth = f(x_smooth)

x_trap = np.linspace(a, b, n + 1)
y_trap = f(x_trap)

dx = (b - a) / n
area = (dx / 2) * (y_trap[0] + 2 * np.sum(y_trap[1:-1]) + y_trap[-1])

st.metric("Estimated Area (พื้นที่โดยประมาณ)", f"{area:.4f}")

fig, ax = plt.subplots()
ax.plot(x_smooth, y_smooth, label="f(x) = x^2 + 1", color="#123f6c", linewidth=2)

for i in range(n):
    ax.plot([x_trap[i], x_trap[i], x_trap[i+1], x_trap[i+1]], 
            [0, y_trap[i], y_trap[i+1], 0], 
            color="#dc8d29", alpha=0.5)
    ax.fill_between([x_trap[i], x_trap[i+1]], 
                    [y_trap[i], y_trap[i+1]], 
                    color="#dc8d29", alpha=0.2)

ax.set(xlabel="x", ylabel="f(x)", title=f"Trapezoidal Rule with n={n}")
ax.grid(alpha=0.25)
ax.legend()
st.pyplot(fig)
plt.close(fig)

if show_table:
    data = pd.DataFrame({"x": x_trap, "f(x)": y_trap})
    st.dataframe(data.round(4), hide_index=True)
    csv = data.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "trapezoidal.csv", "text/csv")
