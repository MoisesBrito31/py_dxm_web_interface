    <template>
    <div>
    <b-overlay rounded="sm" :show="logado">
        <b-form>
        <b-form-group label="Usuário:"
            :state=userOK :invalid-feedback=userInvalido>
            <b-input-group>
                <b-input-group-prepend is-text>
                    <b-icon-person></b-icon-person>
                </b-input-group-prepend>
                <b-form-input id='email'
                    type="text"
                    placeholder="Usuario" v-model="user.email">
                </b-form-input>
            </b-input-group>
        </b-form-group>
        <b-form-group label="Senha:" :state=senhaOK :invalid-feedback=senhaInvalida>
            <b-input-group>
                <b-input-group-prepend is-text>
                    <b-icon-key></b-icon-key>
                </b-input-group-prepend>
                <b-form-input id='senha'
                    :type=senhaType
                    placeholder="Senha" v-model="user.senha">
                </b-form-input>
                <b-button  @mousedown="mostraSenha" :variant=senhaClass> <b-icon icon='brightness-alt-high'></b-icon> </b-button>
            </b-input-group>
        </b-form-group>
        <b-alert
            variant="warning"
            dismissible
            fade
            :show="loginFalha"
            @dismissed="showDismissibleAlert=false">
                Usuário ou Senha Incorreto(s)!
        </b-alert>
        <b-alert
            variant="danger"
            dismissible
            fade
            :show="erro"
            @dismissed="showDismissibleAlert=false">
                falha no servidor [[erroDetalhes]]
        </b-alert>
        <b-form-group class="mt-3 pt-3">
            <b-button @click="chamaLogin" v-bind:class="{disabled:!podelogar}"  block variant="primary">
                <span v-show="espera">
                <b-spinner type="grow" variant="light"></b-spinner>
                <b-spinner type="grow" variant="light"></b-spinner>
                <b-spinner type="grow" variant="light"></b-spinner>
               </span>
               <span v-show="!espera">Login</span>
            </b-button>
        </b-form-group>
    </b-form>
        <template #overlay>
            <div class="text-center">
                <b-icon icon="check-circle" animation="throb" font-scale="5" variant="success"></b-icon>
            </div>
        </template>
    </b-overlay>
</div>
<template>

<script>
export default {
    data(){
        return{
            erroDetalhes:'',
            erro:false,
            logado:false,
            loginFalha: false,
            espera:false,
            senhaType:'password',
            senhaClass:'dark',
            senhaShow: true,
            user:{
                email: '',
                senha: '',
                csrfmiddlewaretoken: this.getCookie('csrftoken')
            }
        }
    },
    props:{
        dominio: String,
    },
    computed:{
        userOK(){
            var valor = this.user.email.length
            return valor>0 && this.user.email.indexOf(' ')<0 
        },
        userInvalido(){
            var valor = this.user.email.length
            if(valor<=0){return "Campo Obrigatorio"}
            else if(this.user.email.indexOf(' ')>0){return "espaço não é permitido"}
            else{return 'ok'}
        },
        senhaOK(){
            return this.user.senha.length>0
        },
        senhaInvalida(){
            if(this.user.senha.length<=0){
                return "senha Necessária!"
            }else{
                return "ok"
            }
        },
        podelogar(){
            return this.userOK && this.senhaOK
        }
    },
    methods:{
        getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },
        chamaLogin(){
            this.loginFalha=false;
            if(this.podelogar){
                this.espera = true
                this.login()
                }
        },
        async login() {
            fetch(`${this.dominio}`,{
                    method: 'post',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCookie('csrftoken'),
                    },
                    body: JSON.stringify(this.user)
            }).then(res=>{
                if(res.status === 200){
                    return res.text()
                }else if(res.status===400) {
                    this.loginFalha=true
                    this.espera=false
                }else{
                    this.erro = true
                    this.espera=false
                    throw 'Erro - servidor fora do ar '
                }
            }).then(result=>{
                 console.log(result)
                    if(result=="ok"){
                        this.logado = true
                        this.$emit('logou',true)
                    }else if(result=="usuario"){
                        this.loginFalha=true
                        this.espera=false
                    }else{
                        this.erro = true
                        this.espera=false
                        throw 'Erro no servidor'
                    }  
            }).catch(erro=>{
                this.erroDetalhes = `--- ${erro}`
                this.erro = true
                this.espera=false
                console.log(erro)
            })
       },
       mostraSenha: function(){
           if(this.senhaShow==true){
               this.senhaShow = false;
               this.senhaClass = 'light';
               this.senhaType = 'text';
           }else{
               this.senhaShow = true;
               this.senhaClass = 'dark';
               this.senhaType = 'password';
           }
       }
    }
}
</script>

  
