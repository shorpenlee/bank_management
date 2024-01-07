import pandas as pd
import streamlit as st

st.title('理财管理	:moneybag:')

test = pd.read_csv('test.txt',sep='\t').sort_values(by=['到期日'])
st.text("")


col1, col2, col3 = st.columns(3)
total_asset = col1.metric(label="总资产", value=test['本金'].sum())
total_count = col2.metric(label="理财数", value=test['本金'].size)



st.divider()

name = st.text_input('名称')
col1, col2, col3 = st.columns(3)
with col1:
	types = st.selectbox('类型',('理财', '定期'))
	days = st.number_input('天数',step=1,format="%.i")
	

with col2:
	banks = st.selectbox('银行',('邮政银行', '中国银行','工商银行'))
	interests = st.number_input('收益率',step=1, format="%g",min_value=0,max_value=10)

with col3:
	values = st.number_input('本金',step=100, format="%.i")
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
				'收益':values*interests/100/365*days}

	test = pd.concat([test, pd.DataFrame([new_row])], ignore_index=True,axis=0)



st.divider()
st.subheader('详情')

def highlight(val):
	if val == '邮政银行':
		return 'background-color: rgba(255, 255, 0, 0.5); font-weight: bold'
	elif val == '中国银行':
		return 'background-color: rgba(0, 0, 255, 0.5); font-weight: bold' 
	elif val == '工商银行':
		return 'background-color: rgba(255, 0, 0, 0.5); font-weight: bold'
	#elif val == '理财':
	#	return 'background-color: rgba(0, 128, 0, 0.5); font-weight: bold'
	#elif val == '定期':
	#	return 'background-color: rgba(128, 0, 128, 0.5); font-weight: bold'
	else:
		return ''

def font_color(val):
	if val == '理财':
		return 'color: green; font-weight: bold'
	elif val == '定期':
		return 'color: orange; font-weight: bold'
	else:
		return ''

st.dataframe(test.style.format('￥{:,.0f}',  subset=["本金","收益"])
						.format('{:,.2f}%',  subset=["收益率"])
						.applymap(highlight)
						.applymap(font_color)

	)



test.to_csv('test.txt', sep='\t', index=False)

hide_streamlit_style = """
			<style>
			#MainMenu {visibility: hidden;}
			footer {visibility: hidden;}
			</style>
			"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 