<template>
	<div>
		<h2>検索ボックス</h2>
		<label for="title">銘柄検索</label>
		<input
			type="text"
			v-model.lazy.trim="eventData.company"
		>
		<button @click="searchCompany">検索</button>
		<br />

		<label for="title">単語検索</label>
		<input
			type="text"
			v-model.lazy.trim="eventData.word"
		>
		<button @click="searchWord">検索</button>

		<br />
		<label for="title">トピック検索</label>
		<input
			type="text"
			v-model.lazy.trim="eventData.topic"
		>
		<button @click="searchTopic">検索</button>

		<highcharts
			class="stock"
			:options="chartOptions"
			ref="chart"
		>
		</highcharts>
		<highcharts 
			:options="barChartOptions"
		>
		</highcharts>
		<table>
			<tbody>
				<tr v-for="(_, idx) in eventData.code.length" :key="idx">
					<td>{{eventData.code[idx]}}</td><td>{{eventData.name[idx]}}</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
		return {
			eventData: {
				code: [],
				name: [],
			},
			chartOptions: {
				title: {
					text: '株価チャート'
				},
				xAxis: {
					categories: [],
					crosshair: true,
					tickInterval: 25
				},
				yAxis: {
					title: false,
					labels: {
						format: '{value}'
					},
					opposite: false,
				},
				series: [],
				// plotOptions: {
				// 	series: {
				// 		events: {
				// 			legendItemClick: function () {
				// 				this.remove(true);
				// 				return false
				// 			}
				// 		}
				// 	}
				// },
			},
			barChartOptions: {
				title: {
					text: '収益率'
				},
				xAxis: {
					categories: ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'],
					crosshair: true,
					tickInterval: 25
				},
				yAxis: {
					title: false,
					labels: {
						format: '{value}' // y軸の目盛り幅が値によって動的に変わる
					},
				},
				series: [],
			}
		}
	},
	beforeCreate() {
		console.log("before create")

		axios.get('http://localhost:8000/company/0000')
		.then(res => {
			if (res.data != null) {
				this.chartOptions.series.push({
					data: res.data.cumR,
					name: '日経平均'
				})
				this.chartOptions.xAxis.categories = res.data.Date

				this.barChartOptions.series.push({
					data: res.data.R,
					name: '日経平均',
					type: 'column'
				})
				this.barChartOptions.xAxis.categories = res.data.Date
			}
		});


		axios.get('http://localhost:8000/company/0001')
		.then(res => {
			if (res.data != null) {
				this.chartOptions.series.push({
					data: res.data.cumR,
					name: 'TOPIX'
				})
				this.chartOptions.xAxis.categories = res.data.Date

				this.barChartOptions.series.push({
					data: res.data.R,
					name: 'TOPIX',
					type: 'column'
				})
				this.barChartOptions.xAxis.categories = res.data.Date
			}
		});

	},
	methods: {
		searchCompany: async function () {
			let res = await axios.get('http://localhost:8000/company/' + this.eventData.company)
	
			if (res.data != null) {
				this.chartOptions.series.push({
					data: res.data.cumR,
					name: this.eventData.company
				})
				this.chartOptions.xAxis.categories = res.data.Date

				this.barChartOptions.series.push({
					data: res.data.R,
					name: this.eventData.company,
					type: 'column'
				})
				this.barChartOptions.xAxis.categories = res.data.Date
			}

		},
		searchWord: async function () {
			let res = await axios.get('http://localhost:8000/word/' + this.eventData.word)
			console.log(res.data)
			if (res.data != null) {
				this.eventData.code = res.data.code
				this.eventData.name = res.data.name
				this.chartOptions.series.push({
					data: res.data.cumR,
					name: this.eventData.word
				})
				this.chartOptions.xAxis.categories = res.data.Date

				this.barChartOptions.series.push({
					data: res.data.R,
					name: this.eventData.word,
					type: 'column'
				})
				this.barChartOptions.xAxis.categories = res.data.Date
			}
		},
		searchTopic: async function () {
			let res = await axios.get('http://localhost:8000/topic/' + this.eventData.topic)
			console.log(res.data)
			if (res.data != null) {
				this.eventData.code = res.data.code
				this.eventData.name = res.data.name
				this.chartOptions.series.push({
					data: res.data.cumR,
					name: this.eventData.topic
				})
				this.chartOptions.xAxis.categories = res.data.Date

				this.barChartOptions.series.push({
					data: res.data.R,
					name: this.eventData.topic,
					type: 'column'
				})
				this.barChartOptions.xAxis.categories = res.data.Date
			}
		}
	}
}
</script>

<style>
td {
	text-align: center;
	vertical-align: top;
}
</style>
