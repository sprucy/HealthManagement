import * as React from 'react';
import { useState } from 'react';
import { Box } from '@mui/material';
import LabelIcon from '@mui/icons-material/Label';
import SettingsSuggestIcon from '@mui/icons-material/SettingsSuggest';
import AnchorOutlinedIcon from '@mui/icons-material/AnchorOutlined';
import AddchartIcon from '@mui/icons-material/Addchart';
import ContentPasteSearchIcon from '@mui/icons-material/ContentPasteSearch';
import MedicalInformationIcon from '@mui/icons-material/MedicalInformation';

import {
    useTranslate,
    DashboardMenuItem,
    MenuItemLink,
    MenuProps,
    useSidebarState,
} from 'react-admin';
import SubMenu from './SubMenu';

import users from "../users";
import groups from "../groups";
import permissions from '../permissions';

import userinfos from "../userinfos";
import bodyinfos from "../bodyinfos";
import smokediabetesinfos from "../smokediabetesinfos";
import bloodpressures from "../bloodpressures";
import bcholesterins from "../bcholesterins";

import bmiscales from "../bmiscales"; 
import indicators from '../indicators';
import riskanalyses from "../riskanalyses";
import healthintervents from "../healthintervents";
import singleassesss from "../singleassesss";
import smokescales from "../smokescales";
import agescales from "../agescales";       
import weightscales from "../weightscales";      
import diabetesscales from "../diabetesscales";
import bloodpressurescales from "../bloodpressurescales";      
import tcscales from "../tcscales";   
import commonriskscales from "../commonriskscales";
import riskevaluatscales from "../riskevaluatscales"; 
  
import dailyhealthassess from "../habitassess";

type MenuName = 'menuSystem' | 'menuData' | 'menuStandard' | 'menuAnalytic' | 'menuEvaluate' ;

const Menu = ({ dense = true }: MenuProps) => {
    const [state, setState] = useState({
        menuData: false,
        menuStandard: false,
        menuAnalytic: false,
        menuEvaluate: false,
        menuSystem: false,
    });
    const translate = useTranslate();
    const [open] = useSidebarState();

    const handleToggle = (menu: MenuName) => {
        setState(state => ({ ...state, [menu]: !state[menu] }));
    };

    return (
        <Box
            sx={{
                width: open ? 200 : 50,
                marginTop: 1,
                marginBottom: 1,
                transition: theme =>
                    theme.transitions.create('width', {
                        easing: theme.transitions.easing.sharp,
                        duration: theme.transitions.duration.leavingScreen,
                    }),
            }}
        >
            <DashboardMenuItem />
            <SubMenu
                handleToggle={() => handleToggle('menuData')}
                isOpen={state.menuData}
                name="health.menu.data"
                icon={<MedicalInformationIcon />}
                dense={dense}
            >
                <MenuItemLink
                    to="/users"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.users.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<users.icon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/userinfos"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.userinfos.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<userinfos.icon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/bodyinfos"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.bodyinfos.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<bodyinfos.icon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/smokediabetesinfos"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.smokediabetesinfos.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<smokediabetesinfos.icon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/bloodpressures"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.bloodpressures.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<bloodpressures.icon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/bcholesterins"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.bcholesterins.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<bcholesterins.icon />}
                    dense={dense}
                />  
            </SubMenu>

            <SubMenu
                handleToggle={() => handleToggle('menuStandard')}
                isOpen={state.menuStandard}
                name="health.menu.standard"
                icon={<AnchorOutlinedIcon />}
                dense={dense}
            >              
                <MenuItemLink
                    to="/bmiscales"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.bmiscales.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<bmiscales.icon />}
                    dense={dense}
                />                                                 
                <MenuItemLink
                    to="/indicators"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.indicators.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<indicators.icon />}
                    dense={dense}
                />  
                <MenuItemLink
                    to="/riskanalyses"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.riskanalyses.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<riskanalyses.icon />}
                    dense={dense}
                />  
                <MenuItemLink
                    to="/healthintervents"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.healthintervents.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<healthintervents.icon />}
                    dense={dense}
                />  
                <MenuItemLink
                    to="/singleassesss"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.singleassesss.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<singleassesss.icon />}
                    dense={dense}
                />  

                <MenuItemLink
                    to="/smokescales"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.smokescales.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<smokescales.icon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/agescales"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.agescales.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<agescales.icon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/weightscales"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.weightscales.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<weightscales.icon />}
                    dense={dense}
                />                
                <MenuItemLink
                    to="/diabetesscales"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.diabetesscales.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<diabetesscales.icon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/bloodpressurescales"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.bloodpressurescales.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<bloodpressurescales.icon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/tcscales"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.tcscales.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<tcscales.icon />}
                    dense={dense}
                /> 
                <MenuItemLink
                    to="/commonriskscales"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.commonriskscales.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<commonriskscales.icon />}
                    dense={dense}
                />                               
                <MenuItemLink
                    to="/riskevaluatscales"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.riskevaluatscales.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<riskevaluatscales.icon />}
                    dense={dense}
                />  
            </SubMenu>
            <SubMenu
                handleToggle={() => handleToggle('menuEvaluate')}
                isOpen={state.menuEvaluate}
                name="health.menu.evaluate"
                icon={<ContentPasteSearchIcon />}
                dense={dense}
            >
                <MenuItemLink
                    to="/habitassess"
                    state={{ _scrollToTop: true }}
                    primaryText="resources.habitassess.name"
                    leftIcon={<LabelIcon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/bmiassess"
                    state={{ _scrollToTop: true }}
                    primaryText="resources.bmiassess.name"
                    leftIcon={<LabelIcon />}
                    dense={dense}
                /> 
                <MenuItemLink
                    to="/bloodpressureassess"
                    state={{ _scrollToTop: true }}
                    primaryText="resources.bloodpressureassess.name"
                    leftIcon={<LabelIcon />}
                    dense={dense}
                /> 
                <MenuItemLink
                    to="/bcholesterinassess"
                    state={{ _scrollToTop: true }}
                    primaryText="resources.bcholesterinassess.name"
                    leftIcon={<LabelIcon />}
                    dense={dense}
                /> 
                <MenuItemLink
                    to="/icvdassess"
                    state={{ _scrollToTop: true }}
                    primaryText="resources.icvdassess.name"
                    leftIcon={<LabelIcon />}
                    dense={dense}
                />                                                
            </SubMenu>
            <SubMenu
                handleToggle={() => handleToggle('menuSystem')}
                isOpen={state.menuSystem}
                name="health.menu.system"
                icon={<AddchartIcon />}
                dense={dense}
            >
                <MenuItemLink
                    to="/groups"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.groups.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<groups.icon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/permissions"
                    state={{ _scrollToTop: true }}
                    primaryText={translate('resources.permissions.name', {
                        smart_count: 2,
                    })}
                    leftIcon={<permissions.icon />}
                    dense={dense}
                />
            </SubMenu>
        </Box>
    );
};

export default Menu;
