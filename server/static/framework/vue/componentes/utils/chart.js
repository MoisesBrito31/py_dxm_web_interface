Vue.component('chart',{
    delimiters: ["[[", "]]"],
    template: `
    <div>   
        <canvas id="chart"></canvas>
    </div>
    `,
    created(){
        setTimeout(()=>{
            this.load()
        },1000)
    },
    data(){
        return{
            config:{
                type: this.type,
                data:{
                    labels: [],
                    datasets: [],
                }
            },
            chart:{},
            chartColors:['#6A5ACD','#00FA9A','#32CD32',
            '#8B4513','#FF0000','#FFD700','#FF69B4',
            '#F5DEB3','#7CFC00','#008080','#0000FF',
            '#DAA520','#FF00FF','#000000']
        }
    },
    props:{
        title:{
            type: String,
            required: false,
            default: "",
        },
        type:{
            type: String,
            required: false,
            default: "line",
        },
        labels:{
            type: String,
            required: false,
            default: "",
        },
        data:{
            type: Array,
            required: false,
            default: ()=>{
                return []
            }
        },
    },
    computed:{        
    },
    methods:{
        resetData(){
            this.config.data.datasets = []
            this.config.data.labels = []
            this.chart.update()
        },
        load(){
            var retorno = this.get_dataset(this.data,this.labels)
            this.config.data.datasets = retorno[0]
            this.config.data.labels = retorno[1]
            var ctx = document.getElementById("chart")
			this.chart = new Chart(ctx, this.config)
        },
        get_dataset(data,label){
            var dataset_conj=[]
            var labels =[]
            try {
                var chaves = Object.keys(data[0])
                var cor_index=0
                chaves.forEach(ele => {
                    if(ele!==label){
                        var dataset_base={
                            label: ele,
                            backgroundColor: this.chartColors[cor_index],
                            borderColor: this.chartColors[cor_index],
                            data: [],
                            fill: false,
                        }
                        cor_index+=1
                        for(var x=0; x<data.length;x++){
                            dataset_base.data.push(data[x][ele])
                        }
                        dataset_conj.push(dataset_base)
                    }else{
                        for(var x=0; x<data.length;x++){
                            labels.push(data[x][ele])
                        }                        
                    }
                })
            } catch (error) {}
            return [dataset_conj,labels]
        },
        refresh(data,label){
            this.resetData()
            var retorno = this.get_dataset(data,label)
            this.config.data.datasets = retorno[0]
            this.config.data.labels = retorno[1]
            this.chart.update()
        }
    },
})