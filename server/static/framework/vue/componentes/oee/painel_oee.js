Vue.component('painel_oee',{
    delimiters: ["[[", "]]"],
    template: `
    <div class="col-auto">
            <div class="bg-light text-center border rounded mb-5 p-2" style="min-width:150px; max-width:250px;" v-on:click="acessaLinha" >
            <div :class="fundo_bg">
                <h3 id="l {{ l.id }}">[[linha.nome]]</h3>
                <div :id="linha.id"></div>
                <h4>
                    <p class="p-2 rounded border border-dark text-center m-auto">
                        <span :class="texto_bg">[[linha.estado]]</span>
                    </p>    
                </h4>  
            </div>          
            </div>
        </div>
    `,
    created(){
        setTimeout(()=>{
            this.gage = new JustGage({
                id: this.id,
                value: this.oee,
                min: 0,
                max: 100,
                title: "OEE",
                symbol: '%',
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
            fundo_bg:"bg-light",
            texto_bg:"text-dark",
            linha: {'id':this.id,'nome':this.nome,'oee':this.oee,'estado':this.status},
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
        id: Number,
        nome: String,
        oee: Number,
        status: String,
    },
    computed:{        
    },
    methods:{
        pisca(){
            if(this.linha.estado=="Parado"){
                if(this.fundo_bg=="bg-danger"){
                    this.fundo_bg="bg-light"
                    this.texto_bg="text-danger"
                }else{
                    this.fundo_bg="bg-danger"
                    this.texto_bg="text-light"
                }
            }else{
                this.fundo_bg="bg-light"
                this.texto_bg="text-success"
            }
        },
        acessaLinha(){
           document.location.href=`/oee/linha/${this.linha.id}`
        },
        refresh(valor,status){
            this.gage.refresh(valor)
            this.linha.estado=status
        }
    },
})