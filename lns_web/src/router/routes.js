import DashboardLayout from "@/layout/dashboard/DashboardLayout.vue";
import HomeLayout from "@/layout/starter/SampleLayout.vue";

// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";
import store from '../store'


// Admin pages
const Login = () => import(/* webpackChunkName: "login" */"@/pages/Login.vue");
const Register = () => import(/* webpackChunkName: "register" */"@/pages/Register.vue");
const Dashboard = () => import(/* webpackChunkName: "dashboard" */"@/pages/Dashboard.vue");
const Profile = () => import(/* webpackChunkName: "common" */ "@/pages/Profile.vue");
const Notifications = () => import(/* webpackChunkName: "common" */"@/pages/Notifications.vue");
const Icons = () => import(/* webpackChunkName: "common" */ "@/pages/Icons.vue");
const Maps = () => import(/* webpackChunkName: "common" */ "@/pages/Maps.vue");
const Typography = () => import(/* webpackChunkName: "common" */ "@/pages/Typography.vue");
const TableList = () => import(/* webpackChunkName: "common" */ "@/pages/TableList.vue");

const isLoggedIn = store.getters["userModule/isUserLoggedIn"];
console.log("User logged in: ", isLoggedIn)
console.log(isLoggedIn==true)
let routes;
if (isLoggedIn === true) {
  routes = [
    {
      path: "/",
      component: DashboardLayout,
      redirect: "/dashboard",
      children: [
        {
          path: "dashboard",
          name: "dashboard",
          component: Dashboard,
        },
        {
          path: "profile",
          name: "profile",
          component: Profile
        },
        {
          path: "notifications",
          name: "notifications",
          component: Notifications
        },
        {
          path: "icons",
          name: "icons",
          component: Icons
        },
        {
          path: "maps",
          name: "maps",
          component: Maps
        },
        {
          path: "typography",
          name: "typography",
          component: Typography
        },
        {
          path: "table-list",
          name: "table-list",
          component: TableList
        }
      ]
    },
    { path: "*", component: NotFound },
  ]
} else {
  // Do like above, a "LoginLayout"? or "LandingLayout" and has children like Login, Register, Forgot, TOS, FAQ, etc..?
  routes = [{
    path: "/",
    component: HomeLayout,
    redirect: "/login",
      children: [
        {
          path: "login",
          name: "login",
          component: Login,
        },
        {
          path: "register",
          name: "register",
          component: Register
        },
        // {
        //   path: "forgot-password",
        //   name: "forgot-password",
        //   component: ForgotPassword
        // }
        // {
        //   path: "reset-password",
        //   name: "reset-password",
        //   component: ResetPassword
        // }
      ]
  },
  { path: "*", component: NotFound },
  ]
}

/**
 * Asynchronously load view (Webpack Lazy loading compatible)
 * The specified component must be inside the Views folder
 * @param  {string} name  the filename (basename) of the view to load.
function view(name) {
   var res= require('../components/Dashboard/Views/' + name + '.vue');
   return res;
};**/

export default routes;
