Vue.component('main_menu',{
  delimiters: ["[[", "]]"],
  template:`
    <div>
         <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand>
      <img class="mr-3" src="/static/img/logo-e-service.png" width="120" height="40">
    </b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item href="/">Home</b-nav-item>
        <b-nav-item href="/oee">Fábrica</b-nav-item>
        <b-nav-item href="/config">Configurar</b-nav-item>
        <b-nav-item href="/sobre">Sobre</b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav right>
        <b-nav-form v-if="script_falha">
          <span><strong>DXM Descalibrado</strong></span>
          <img src="/static/img/alerta.png" width="30" height="30" />
        </b-nav-form>
        <b-nav-form right>
          <img :src="dxm_online" width="30" height="30" />
        </b-nav-form>

        <b-nav-item-dropdown right>
          <!-- Using 'button-content' slot -->
          <template #button-content>
            <em>User</em>
          </template>
          <b-dropdown-item href="#">Profile</b-dropdown-item>
          <b-dropdown-item href="#">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
    </div>
    `,
    created(){
      this.load()
    },
    methods:{
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
        }).catch(erro=>{
            console.log(erro)
        })
      }
    },
    data(){
      return{
        data:[],
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
          return "static/img/notifiOk.ico";
        }else{
          return "static/img/notifiFalha.ico";W
        }
      }
    },
    props:{
    },
})


