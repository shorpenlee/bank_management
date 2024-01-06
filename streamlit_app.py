import pandas as pd
import streamlit as st

st.title('理财管理	:moneybag:')

test = pd.read_csv('test.txt',sep='\t')

with st.sidebar:
	name = st.text_input('名称')
	types = st.selectbox('类型',('理财', '定期'))
	banks = st.selectbox('银行',('邮政银行', '中国银行','工商银行'))
	days = st.number_input('天数',step=1,format="%.i")
	values = st.number_input('本金',step=100, format="%.i")
	interests = st.number_input('收益率',step=0.01, format="%g",min_value=0.00,max_value=1.00)
	start_date = st.date_input('起始日',value="today",format="YYYY/MM/DD")
	st.text("")
	st.text("")

	# Add record to dataframe
	if st.button('添加新项'):
	    new_row = {'名称': name,
	    			'类型':types,
	    			'银行':banks,
	    			'天数':days,
	    			'本金':values,
	    			'收益率':interests,
	    			'起始日':start_date,
	    			'到期日':start_date,
	    			'收益':values*interests/365*days}

	    test = pd.concat([test, pd.DataFrame([new_row])], ignore_index=True,axis=0)


st.divider()
st.header('详情')


st.dataframe(test,
	column_config={
	"本金": st.column_config.NumberColumn(
            "本金",
            min_value=0,
            step=1,
            format="￥%.2d",
        ),
	"收益": st.column_config.NumberColumn(
            "收益",
            format="￥%.2d",
        )

	}
	)
test.to_csv('test.txt', sep='\t', index=False)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 