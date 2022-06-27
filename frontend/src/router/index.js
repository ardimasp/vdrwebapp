import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err);
}

const routes = [
  {
    path: '/',
    redirect: 'vtkviewer',
  },
  {
    path: '/vtkviewer',
    name: 'vtkviewer',
    component: () => import('@/views/viewer/VtkViewer.vue'),
  },
  {
    path: '/viewer',
    name: 'viewer',
    component: () => import('@/views/viewer/Viewer.vue'),
  },
  {
    path: '/filemanagement',
    name: 'file-management',
    component: () => import('@/views/file-management/Folder.vue'),
  },
  {
    path: '/maps',
    name: 'maps',
    component: () => import('@/views/map/Maps.vue'),
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('@/views/dashboard/Dashboard.vue'),
  },
  {
    path: '/map-showcase',
    name: 'mapShowcase',
    component: () => import('@/views/showcase/MapShowcase.vue'),
  },
  {
    path: '/showcase',
    name: 'showcase',
    component: () => import('@/views/showcase/FormLayouts.vue'),
  },
  {
    path: '/vtp-form',
    name: 'vtpForm',
    component: () => import('@/views/map/VTPFormLayout.vue'),
  },
  {
    path: '/production',
    name: 'production',
    component: () => import('@/views/sreeya/Sreeya.vue'),
  },
  {
    path: '/production/prediction',
    name: 'production-prediction',
    component: () => import('@/views/sreeya/SreeyaPrediction.vue'),
  },
  {
    path: '/not-authorized',
    name: 'not-authorized',
    component: () => import('@/views/sreeya/NotAuthorized.vue'),
  },
  {
    path: '/test',
    name: 'testtt-HELP',
    component: () => import('@/views/test/testing.vue'),
    meta: {layout: "blank"}
  },
  {
    path: '/typography',
    name: 'typography',
    component: () => import('@/views/typography/Typography.vue'),
  },
  {
    path: '/icons',
    name: 'icons',
    component: () => import('@/views/icons/Icons.vue'),
  },
  {
    path: '/cards',
    name: 'cards',
    component: () => import('@/views/cards/Card.vue'),
  },
  {
    path: '/simple-table',
    name: 'simple-table',
    component: () => import('@/views/simple-table/SimpleTable.vue'),
  },
  {
    path: '/form-layouts',
    name: 'form-layouts',
    component: () => import('@/views/form-layouts/FormLayouts.vue'),
  },
  {
    path: '/pages/account-settings',
    name: 'pages-account-settings',
    component: () => import('@/views/pages/account-settings/AccountSettings.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/pages/Login.vue'),
    meta: {
      layout: 'blank',
    },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/pages/Register.vue'),
    meta: {
      layout: 'blank',
    },
  },
  {
    path: '/error-404',
    name: 'error-404',
    component: () => import('@/views/Error.vue'),
    meta: {
      layout: 'blank',
    },
  },
  {
    path: '*',
    redirect: 'error-404',
  },
  {
    path: '/profile/:userid',
    name: "profile",
    component: () => import("@/views/profile/Profile.vue"),
    meta: {
      layout: 'top',
    },
  },
  {
    path: '/admin',
    name: "admin",
    component: () => import("@/views/admin/Admin.vue"),
    meta: {
      layout: 'top',
    },
  },
  {
    path: '/admin/adduser',
    name: "admin_adduser",
    component: () => import("@/views/admin/addUser.vue"),
    meta: {
      layout: 'top',
    },
  },
  {
    path: '/admin/profile/:userid',
    name: "admin_edituser",
    component: () => import("@/views/admin/editUser.vue"),
    meta: {
      layout: 'top',
    },
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
})

router.beforeEach((to, from, next) => {
  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user');

  // trying to access a restricted page + not logged in
  // redirect to login page
  if (authRequired && !loggedIn) next('/login');
  else next();
  
});

export default router
