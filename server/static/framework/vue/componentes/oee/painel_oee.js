Vue.component('painel_oee',{
    delimiters: ["[[", "]]"],
    template: `
    <div >
            <div :class="fundo_bg" style="min-width:150px; max-width:250px;" v-on:click="acessaLinha" >
                <h3 id="l {{ l.id }}">[[linha.nome]]</h3>
                <gage :anima=true ref="gage" :id="linha.id" title="OEE" symbol="%" ></gage>
                <h4>
                    <p class="p-2 rounded border border-dark text-center m-auto">
                        <span :class="texto_bg">[[linha.estado]]</span>
                    </p>    
                </h4>  
            </div>                
    </div>
    `,
    created(){
        setInterval(() => {
            this.pisca()
        }, 1000);
    },
    data(){
        return{
            fundo_bg:"bg-light text-center border rounded mb-5 p-2",
            texto_bg:"text-dark",
            linha: {'id':this.id,'nome':this.title,'oee':this.oee,'estado':this.status},
        }
    },
    props:{
        id: {
            type: [String,Number],
            required: true,
        },
        title:{
            type: String,
            required: false,
            default: "",
        },
        oee:{
            type: Number,
            required: false,
            default: 0,
        },
        status:{
            type: String,
            required: false,
            default: "Parado",
        },
    },
    computed:{        
    },
    methods:{
        pisca(){
            if(this.linha.estado=="Parado"){
                this.$refs.gage.emit_alerta(true)
                if(this.fundo_bg=="bg-danger text-center border rounded mb-5 p-2"){
                    this.fundo_bg="bg-light text-center border rounded mb-5 p-2"
                    this.texto_bg="text-danger"
                }else{
                    this.fundo_bg="bg-danger text-center border rounded mb-5 p-2"
                    this.texto_bg="text-light"
                }
            }else{
                this.$refs.gage.emit_alerta(false)
                this.fundo_bg="bg-light text-center border rounded mb-5 p-2"
                this.texto_bg="text-success"
            }
        },
        acessaLinha(){
           document.location.href=`/oee/linha/${this.linha.id}`
        },
        refresh(valor,status){
            this.$refs.gage.refresh(valor)
            this.linha.estado=status
        }
    },
})