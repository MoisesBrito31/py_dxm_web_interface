Vue.component('painel_oee',{
    delimiters: ["[[", "]]"],
    template: `
    <b-col sm="4">
        <b-row >[[linha.nome]]</b-row>
        <b-row id="GAGE"></b-row>
        <b-row>[[linha.estado]]</b-row>
    </b-col>
    `,
    created(){
        setTimeout(()=>{
            this.gage = new JustGage({
                id: "GAGE",
                value: this.oee,
                min: 0,
                max: 100,
                title: "OEE",
                symbol: '%',
                pointer: true,
                customSectors: this.sectors,
                relativeGaugeSize: true
            })
            //this.gage.refresh(this.linha.oee)
        },100)
    },
    data(){
        return{
            linha: {'nome':this.nome,'oee':this.oee,'estado':this.status},
            gage: {},
            sectors: [{
                color: "#c00002",
                lo: 0,
                hi: 20,
            }, {
                color: "#febf00",
                lo: 20,
                hi: 40,
            }, {
                color: "#fdf500",
                lo: 40,
                hi: 60,
            }, {
                color: "#92d14f",
                lo: 60,
                hi: 80,
            }, {
                color: "#00af50",
                lo: 80,
                hi: 100,
            }],
        }
    },
    props:{
        nome: String,
        oee: Number,
        status: String,
    },
    computed:{
    },
    methods:{
    },
})