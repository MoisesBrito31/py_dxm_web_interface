Vue.component('painel_oee',{
    delimiters: ["[[", "]]"],
    template: `
    <div>
        <b-col cols="2">
            <b-row>[[linha.nome]]</b-row>
            <b-row>[[linha.oee]]</b-row>
            <b-row>[[linha.estado]]</b-row>
        </b-col>
    </div>
    `,
    data(){
        return{
            linha: this.p_linha
        }
    },
    props:{
        p_linha:{}
    },
    computed:{
    },
    methods:{
    },
})