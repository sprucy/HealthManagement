import polyglotI18nProvider from 'ra-i18n-polyglot';
import KitchenIcon from "@mui/icons-material/Kitchen";
import { Box } from "@mui/material";
import { Admin, Resource, CustomRoutes, List } from "react-admin";
import drfProvider, { tokenAuthProvider, fetchJsonWithAuthToken, jwtTokenAuthProvider, fetchJsonWithAuthJWTToken } from 'ra-data-django-rest-framework';
import { Route } from "react-router-dom";

import englishMessages from './i18n/en';
import customChineseMessages from './i18n/zh';
import Layout from "./layout/Layout";

import users from "./users";
import groups from "./groups";
import permissions from './permissions';
import userinfos from "./userinfos";
import smokediabetesinfos from "./smokediabetesinfos";
import bodyinfos from "./bodyinfos";
import bloodpressures from "./bloodpressures";
import bcholesterins from "./bcholesterins";
import indicators from './indicators';
import agescales from "./agescales";       
import weightscales from "./weightscales";      
import bloodpressurescales from "./bloodpressurescales";      
import tcscales from "./tcscales";   
import smokescales from "./smokescales";
import diabetesscales from "./diabetesscales";
import riskevaluatscales from "./riskevaluatscales"; 
import commonriskscales from "./commonriskscales";
import bmiscales from "./bmiscales"; 
import singleassesss from "./singleassesss";  
import riskanalyses from "./riskanalyses"; 
import healthintervents from "./healthintervents";

import HabitAssess from "./habitassess/HabitAssess";
import BMIWeightAssess from './bmiassess/BMIWeightAssess';
import BPAssess from "./bloodpressureassess/BPAssess";
import BcholesterinAssess from "./bcholesterinassess/BcholesterinAssess";
import ICVDAssess from './icvdassess/ICVDAssess';
import Dashboard from "./dashboard/Dashboard";

const i18nProvider = polyglotI18nProvider(
  locale => {
      if (locale === 'en') {
          return englishMessages;
      }else if (locale === 'zh') {
        return customChineseMessages;
    }
    // Always fallback on english
    return englishMessages; // 直接返回英语消息对象
},
  'en', // Default locale
  [
      { locale: 'en', name: 'English' },
      { locale: 'zh', name: '中文' },
  ]
);

let dataProvider: any;
let authProvider: any;
const useJWTAuth = import.meta.env.VITE_APP_USE_JWT_AUTH;
const serverUrl = import.meta.env.VITE_SERVER_URL;

if (useJWTAuth) {
    console.log("Using rest_framework_simplejwt.authentication.JWTAuthentication");
    authProvider = jwtTokenAuthProvider({obtainAuthTokenUrl: serverUrl+"/api/token/"});
    dataProvider = drfProvider(serverUrl+"/api", fetchJsonWithAuthJWTToken);
} else {
    console.log("Using rest_framework.authentication.TokenAuthentication");
    authProvider = tokenAuthProvider();
    dataProvider = drfProvider(serverUrl+"/api", fetchJsonWithAuthToken);
}


export const App = () => (
  <Admin 
    authProvider={authProvider} 
    dataProvider={dataProvider} 
    i18nProvider={i18nProvider}
    title={
      <Box display="flex" gap={1} alignItems="center">
        <KitchenIcon /> Health Manage App
      </Box>
    }
    dashboard={Dashboard}
    layout={Layout}
    defaultTheme="light" >

    <Resource name="users" {...users} />  
    <Resource name="userinfos" {...userinfos} />
    <Resource name="groups" {...groups} /> 
    <Resource name="permissions" {...permissions} />
    <Resource name="smokediabetesinfos" {...smokediabetesinfos} />
    <Resource name="bodyinfos" {...bodyinfos} />
    <Resource name="bloodpressures" {...bloodpressures} />
    <Resource name="bcholesterins" {...bcholesterins} />
    <Resource name="indicators" {...indicators} />      
    <Resource name="agescales" {...agescales} />       
    <Resource name="weightscales" {...weightscales} />      
    <Resource name="bloodpressurescales" {...bloodpressurescales} />      
    <Resource name="tcscales" {...tcscales} />   
    <Resource name="smokescales" {...smokescales} />
    <Resource name="diabetesscales" {...diabetesscales} />
    <Resource name="riskevaluatscales" {...riskevaluatscales} /> 
    <Resource name="commonriskscales" {...commonriskscales} />
    <Resource name="bmiscales" {...bmiscales} /> 
    <Resource name="singleassesss" {...singleassesss} />  
    <Resource name="riskanalyses" {...riskanalyses} /> 
    <Resource name="healthintervents" {...healthintervents} />

    <Resource name="habitassess" list={HabitAssess} />
    <Resource name="bmiassess" list={BMIWeightAssess} />
    <Resource name="bloodpressureassess" list={BPAssess} />
    <Resource name="bcholesterinassess" list={BcholesterinAssess} />
    <Resource name="icvdassess" list={ICVDAssess} />    
  </Admin>
);
