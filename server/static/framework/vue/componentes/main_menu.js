Vue.component('main_menu',{
  delimiters: ["[[", "]]"],
  template:`
    <div>
    <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand href="#">
      <img class="mr-3" src="/static/img/logo-e-service.png" width="120" height="40">
    </b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item href="/">Início</b-nav-item>
        <b-nav-item href="/oee">Fábrica</b-nav-item>
        <b-nav-item href="/config">Configurar</b-nav-item>
        <b-nav-item href="/about">Sobre</b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto mr-2" v-if="!erro">
        <b-nav-form v-if="script_falha">
          <span class="text-warning m-auto p-2"><strong>DXM Descalibrado</strong></span>
          <img class="m-auto" src="/static/img/alerta.png" width="30" height="30" />
        </b-nav-form>

        <b-nav-item-dropdown right>
          <template #button-content>
            <em><img :src="dxm_online" width="30" height="30" /> </em>
          </template>
          <b-dropdown-item href="#">
            <button type="button" class="btn btn-light p-1 mr-2">
              <img src="/static/img/sync.png" width="20" height="20" />
            </button>
          </b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item-dropdown right>
          <template #button-content>
            <em>[[user]]</em>
          </template>
          <b-dropdown-item href="#">Perfil</b-dropdown-item>
          <b-dropdown-item href="/logout">logout</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
    </div>
    `,
    created(){
      this.load()
      setInterval(()=>{this.load()},2000)
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
      load(){
        this.readData()
      },
      async readData() {
        fetch('/config/online',{
                method: 'get',
                headers: {
                    'Content-Type': 'application/json',
                }
        }).then(res=>{
            if(res.status === 200){
                return res.text()
            }
        }).then(result=>{
             console.log(result)
             this.data = JSON.parse(result)
             this.erro= false
        }).catch(erro=>{
            console.log(erro)
            this.erro= true
        })
      }
    },
    data(){
      return{
        data:[],
        user: this.getCookie("userName"),
        erro: true,
      }
    },
    computed:{
      script_falha(){
        if(this.data.script==="ok"){
          return false;
        }else{
          return true;
        }
      },
      dxm_online(){
        if(this.data.dxm_online==="True"){
          return "/static/img/notifiOk.ico";
        }else{
          return "/static/img/notifiFalha.ico";W
        }
      }
    },
    props:{
    },
})


