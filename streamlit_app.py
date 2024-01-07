import pandas as pd
import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime


st.title('理财管理	:moneybag:')

test = pd.read_csv('test.txt',sep='\t').sort_values(by=['到期日'])
st.text("")

# metrics

col1, col2, col3 = st.columns(3)
total_asset = col1.metric(label="总资产", value=test['本金'].sum())
total_count = col2.metric(label="理财数", value=test['本金'].size)
st.divider()

# add new items

st.subheader('新增')

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

## data display


st.subheader('表格视图')

st.text("")
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


st.divider()

##日历


st.subheader('日历视图')


#FF6C6C
#FFBD45
#FF4B4B
#FF6C6C
#FFBD4


bank_color = {"邮政银行":"#FF6C6C",
			 "工商银行":"#FFBD45",
			 "中国银行":"#FFBD4",
             }

events = []
for i in range(len(test)):
    event = {
        'title': test['银行'][i] + '|' + test['类型'][i] + '|' + test['名称'][i]  + '|' + str(test['本金'][i]) ,
        'color': bank_color[test['银行'][i]],
        'start': test['到期日'][i]#datetime.strptime(test['到期日'][i], '%m/%d/%Y').date().strftime("%Y-%m-%d")
    }
    events.append(event)

# Print the list of dictionaries
print(events)

calendar_options = {
"editable": "false",
"navLinks": "true",
"selectable": "true",
"headerToolbar": {
		"left": "today prev,next",
		"center": "title",
		"right": "dayGridDay,dayGridWeek,dayGridMonth",
		},
"buttonText":{
		  "today":"今日",
		  "prev":"向前",
		  "next":"向后",
		  "dayGridDay":"日",
		  "dayGridWeek":"周",
		  "dayGridMonth":"月",
		},
"initialDate": datetime.now().strftime("%Y-%m-%d"),
"initialView": "dayGridMonth",
        }

state = calendar(
    events=st.session_state.get("events", events),
    options=calendar_options,
    custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
    .fc-event-title {
	padding: 0 1px;
	white-space: normal;
	}
    """,
    key='daygrid',
)

if state.get("eventsSet") is not None:
    st.session_state["events"] = state["eventsSet"]

#st.write(state)

## end

hide_streamlit_style = """
			<style>
			#MainMenu {visibility: hidden;}
			footer {visibility: hidden;}
			</style>
			"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 