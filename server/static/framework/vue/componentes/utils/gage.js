Vue.component('gage',{
    delimiters: ["[[", "]]"],
    template: `
    <div :class="fundo_bg">   
        <div :id="id"></div>
    </div>
    `,
    created(){
        setTimeout(()=>{
            this.gage = new JustGage({
                id: this.id,
                value: this.value,
                donut: this.cicle,
                min: this.min,
                counter: this.anima,
                max: this.max,
                title: this.title,
                symbol: this.symbol,
                pointer: true,
                customSectors: this.sectors,
                relativeGaugeSize: true
            })
        },100)
        setInterval(() => {
            this.pisca()
        }, 1000);
    },
    data(){
        return{
            alerta:false,
            fundo_bg:"bg-light",
            gage: {},
            sectors: [{
                color: "#c00002",
                lo: this.min,
                hi: parseInt((this.max-this.min)*0.2),
            }, {
                color: "#febf00",
                lo: parseInt((this.max-this.min)*0.2),
                hi: parseInt((this.max-this.min)*0.4),
            }, {
                color: "#fdf500",
                lo: parseInt((this.max-this.min)*0.4),
                hi: parseInt((this.max-this.min)*0.6),
            }, {
                color: "#92d14f",
                lo: parseInt((this.max-this.min)*0.6),
                hi: parseInt((this.max-this.min)*0.8),
            }, {
                color: "#00af50",
                lo: parseInt((this.max-this.min)*0.8),
                hi: this.max,
            }]
        }
    },
    props:{
        id: {
            type: String,
            required: true,
        },
        anima:{
            type: Boolean,
            required: false,
            default: false,
        },
        cicle:{
            type: Boolean,
            required: false,
            default: false,
        },
        value: {
            type: Number,
            required: false,
            default: 0,
        },
        title:{
            type: String,
            required: false,
            default: "",
        },
        symbol:{
            type: String,
            required: false,
            default: "",
        },
        min:{
            type: Number,
            required: false,
            default: 0,
        },
        max:{
            type: Number,
            required: false,
            default: 100,
        },
    },
    computed:{        
    },
    methods:{
        pisca(){
            if(this.alerta){
                if(this.fundo_bg=="bg-danger"){
                    this.fundo_bg="bg-light"
                }else{
                    this.fundo_bg="bg-danger"
                }
            }else{
                this.fundo_bg="bg-light"
            }
        },
        refresh(valor){
            this.gage.refresh(valor)
        },
        emit_alerta(valor){
            if(valor){
                this.alerta=true
            }else{
                this.alerta=false
            }
        }
    },
})