import { TranslationMessages } from 'react-admin';
import englishMessages from 'ra-language-english';
import { permission } from 'process';


const customEnglishMessages: TranslationMessages = {
    ...englishMessages,
    health: {
        search: 'Search',
        configuration: 'Configuration',
        language: 'Language',
        theme: {
            name: 'Theme',
            light: 'Light',
            dark: 'Dark',
        },
        systemuserwarning:'system manage user, no personal health information data!',
        dashboard: {
            title: 'Dashboard',            
            monthly_revenue: 'Monthly Revenue',
            month_history: '30 Day Revenue History',
            new_orders: 'New Orders',
            pending_reviews: 'Pending Reviews',
            all_reviews: 'See all reviews',
            new_customers: 'New Customers',
            all_customers: 'See all customers',
            pending_orders: 'Pending Orders',
            order: {
                items: 'by %{customer_name}, one item |||| by %{customer_name}, %{nb_items} items',
            },
            welcome: {
                title: 'Welcome to the react-admin e-commerce demo',
                subtitle:
                    "This is the admin of an imaginary poster shop. Feel free to explore and modify the data - it's local to your computer, and will reset each time you reload.",
                ra_button: 'react-admin site',
                demo_button: 'Source for this demo',
            },
        },
        bmiassess: {
            heightchart:'Height Chart',
            weightchart:'Weight Chart',
            bmichart: 'BMI Chart',
            waistchart: 'Waist Chart',            
            weekweight: 'Week Average Weight',
            weekbmi: 'Week Average BMI',
            weekwaist: 'Week Average Waist',
        },
        bloodpressureassess: {
            charttitle: 'Blood Pressure Measurement Chart',
            measuretime: 'Measure Time',
            dbp: 'DBP',
            sbp: 'SBP',
            hr: 'HR',            
            avgdbp: 'average DBP',
            avgsbp: 'average SBP',
            avghr: 'average HR',
        },
        bcholesterinassess: {
            charttitle: 'Bcholesterin Measurement Chart',
            measuretime: 'Measure Time',          
            tc: 'TC',
            ldl: 'LDL',
            hdl: 'HDL',
            tg: 'TG',             
            avgtc: 'average TC',
            avgldl: 'average LDL',
            avghdl: 'average HDL',
            avgtg: 'average TG',
        },
        icvdassess:{
            minrisk: 'The lowest absolute risk of onset at 10 years in the same age',
            avgrisk: 'Mean absolute risk of onset over 10 years for the same age',
            currisk: 'I assess the absolute risk of developing the disease in 10 years',
        },                        
        menu: {
            system: 'System Manage',
            data: 'Health Information',
            analytic: 'Health Analytic',
            standard: 'Standard Manage',
            evaluate: 'Health Evaluate',
        },
        events: {
            review: {
                title: 'Posted review on "%{product}"',
            },
            order: {
                title: 'Ordered 1 poster |||| Ordered %{smart_count} posters',
            },
        },
    },
    resources: {
        users: {
            name: 'User |||| Users',
            fields: {
                username: 'username',
                first_name: 'first name',
                last_name: 'last name',
                email: 'email',
                last_login: 'last login',
                date_joined: 'date joined',
                is_superuser: 'superuser',
                is_staff:'staff',
                is_active: 'active',
                groups: 'groups',
                password: 'password',
                confirm_password: 'confirm password',
                user_permissions: 'user permissions',
            },
            filters: {
                last_visited: 'Last visited',
                today: 'Today',
                this_week: 'This week',
                last_week: 'Last week',
                this_month: 'This month',
                last_month: 'Last month',
                earlier: 'Earlier',
                has_ordered: 'Has ordered',
                has_newsletter: 'Has newsletter',
                group: 'Segment',
            },
            fieldGroups: {
                identity: 'Identity',
                address: 'Address',
                stats: 'Stats',
                history: 'History',
                password: 'Password',
                permissions: 'permissions',
                change_password: 'Change Password',
            },
            page: {
                delete: 'Delete Customer',
            },
            errors: {
                password_mismatch:
                    'The password confirmation is not the same as the password.',
            },
            notifications: {
                created:
                    'Customer created |||| %{smart_count} customers created',
                updated:
                    'Customer updated |||| %{smart_count} customers updated',
                deleted:
                    'Customer deleted |||| %{smart_count} customers deleted',
            },
        },
        groups: {
            name: 'Group |||| Groups',
            title: 'Group %{reference}',
            fields: {
                id: 'ID',
                name: 'Name',
                permissions: 'Permissions',
            },
            notifications: {
                created:
                    'Group created |||| %{smart_count} groups created',
                updated: 'Group updated |||| %{smart_count} groups updated',
                deleted: 'Group deleted |||| %{smart_count} groups deleted',
            },
        },
        permissions: {
            name: 'Permission |||| Permissions',
            fields: {
                id: 'ID',
                name: 'Name',
                codename: 'Codename',
                content_type: 'Content Type',
            },
            notifications: {
                created:
                    'Permission created |||| %{smart_count} permissions created',
                updated:
                    'Permission updated |||| %{smart_count} permissions updated',
                deleted:
                    'Permission deleted |||| %{smart_count} permissions deleted',
            },
        },
        userinfos: {
            name: 'Base Information',
            fields: {
                user: 'User',
                ssn: 'ssn',
                birthday: 'Birthday',
                sex: 'Sex',
                phone: 'Phone',
                province: 'Province',
                city: 'City',
                company: 'Company',
                org: 'Org',
                address: 'Address',
                photo: 'Photo',
            },
            notifications: {
                created:
                    'Base Information created |||| %{smart_count} Base Information created',
                updated:
                    'Base Information updated |||| %{smart_count} Base Information updated',
                deleted:
                    'Base Information deleted |||| %{smart_count} Base Information deleted',
            },
        },
        agescales: {
            name: 'Age Scales',
            fields: {
                id: 'Scales ID',
                sex: 'Sex',
                maxv: 'Max Value',
                score: 'Score',
            },
            notifications: {
                created: 'Age Scales created |||| %{smart_count} Age Scales created',
                updated: 'Age Scales updated |||| %{smart_count} Age Scales updated',
                deleted: 'Age Scales deleted |||| %{smart_count} Age Scales deleted',
            },
        },
        bodyinfos: {
            name: 'Body Information',
            fields: {
                id: 'ID',
                user: 'User',
                measuretime: 'Measure Time',
                height: 'Height',
                weight: 'Weight',
                waist: 'Waist',
            },
            notifications: {
                created: 'Smoke Diabetes information created |||| %{smart_count} Smoke Diabetes information created',
                updated: 'Smoke Diabetes information updated |||| %{smart_count} Smoke Diabetes information updated',
                deleted: 'Smoke Diabetes information deleted |||| %{smart_count} Smoke Diabetes information deleted',
            },
        },   
        smokediabetesinfos: {
            name: 'Smoke Diabetes',
            fields: {
                id: 'ID',
                user: 'User',
                smoke: 'Smoke',
                smokestart: 'Smoke Start',
                drink: 'Drink',
                drinkstart: 'Drink Start',
                diabetes: 'Diabetes',
                diabetesstart: 'Diabetes Start',
            },
            notifications: {
                created: 'Smoke Diabetes information created |||| %{smart_count} Smoke Diabetes information created',
                updated: 'Smoke Diabetes information updated |||| %{smart_count} Smoke Diabetes information updated',
                deleted: 'Smoke Diabetes information deleted |||| %{smart_count} Smoke Diabetes information deleted',
            },
        },
        bloodpressures: {
            name: 'Bloodpressures',
            fields: {
                id: 'ID',
                user: 'User',
                measuretime: 'Measure Time',
                DBP: 'DBP',
                SBP: 'SBP',
                HR: 'HR',
            },
            notifications: {
                created: 'Bloodpressures Information created |||| %{smart_count} Bloodpressures Information created',
                updated: 'Bloodpressures Information updated |||| %{smart_count} Bloodpressures Information updated',
                deleted: 'Bloodpressures Information deleted |||| %{smart_count} Bloodpressures Information deleted',
            },
        },
        bcholesterins: {
            name: 'Bcholesterins',
            fields: {
                id: 'ID',
                user: 'User',
                measuretime: 'Measure Time',
                TC: 'TC',
                LDL: 'LDL',
                HDL: 'HDL',
                TG: 'TG',
            },
            notifications: {
                created: 'Bcholesterins Information created |||| %{smart_count} Bcholesterins Information created',
                updated: 'Bcholesterins Information updated |||| %{smart_count} Bcholesterins Information updated',
                deleted: 'Bcholesterins Information deleted |||| %{smart_count} Bcholesterins Information deleted',
            },
        },
        bmiscales: {
            name: 'BMI Scales',
            fields: {
                id: 'ID',
                bmi: 'BMI',
                wtype: 'Wtype',
            },
            notifications: {
                created: 'BMI Scales created |||| %{smart_count} BMI Scales created',
                updated: 'BMI Scales updated |||| %{smart_count} BMI Scales updated',
                deleted: 'BMI Scales deleted |||| %{smart_count} BMI Scales deleted',
            },
        },
        diabetesscales: {
            name: 'Diabetes Scales',
            fields: {
                id: 'ID',
                sex: 'Sex',
                diabetes: 'Diabetes',
                score: 'Score',
            },
            notifications: {
                created: 'Diabetes Scales created |||| %{smart_count} Diabetes Scales created',
                updated: 'Diabetes Scales updated |||| %{smart_count} Diabetes Scales updated',
                deleted: 'Diabetes Scales deleted |||| %{smart_count} Diabetes Scales deleted',
            },
        },
        riskevaluatscales: {
            name: 'Risk evaluate',
            fields: {
                id: 'ID',
                sex: 'Sex',
                score: 'Score',
                risk: 'Risk%',
            },
            notifications: {
                created: 'Risk evaluate Scales created |||| %{smart_count} Risk evaluate Scales created',
                updated: 'Risk evaluate Scales updated |||| %{smart_count} Risk evaluate Scales updated',
                deleted: 'Risk evaluate Scales deleted |||| %{smart_count} Risk evaluate Scales deleted',
            },
        },
        weightscales: {
            name: 'Weight Scales',
            fields: {
                id: 'ID',
                sex: 'Sex',
                maxv: 'Max Value',
                score: 'Score',
            },
            notifications: {
                created: 'Weight Scales created |||| %{smart_count} Weight Scales created',
                updated: 'Weight Scales updated |||| %{smart_count} Weight Scales updated',
                deleted: 'Weight Scales deleted |||| %{smart_count} Weight Scales deleted',
            },
        },
        bloodpressurescales: {
            name: 'Bloodpressure',
            fields: {
                id: 'ID',
                sex: 'Sex',
                maxv: 'Max Value',
                score: 'Score',
            },
            notifications: {
                created: 'Bloodpressure Scales created |||| %{smart_count} Bloodpressure Scales created',
                updated: 'Bloodpressure Scales updated |||| %{smart_count} Bloodpressure Scales updated',
                deleted: 'Bloodpressure Scales deleted |||| %{smart_count} Bloodpressure Scales deleted',
            },
        },
        tcscales: {
            name: 'TC Scales',
            fields: {
                id: 'ID',
                sex: 'Sex',
                maxv: 'Max Value',
                score: 'Score',
            },
            notifications: {
                created: 'TC Scales created |||| %{smart_count} TC Scales created',
                updated: 'TC Scales updated |||| %{smart_count} TC Scales updated',
                deleted: 'TC Scales deleted |||| %{smart_count} TC Scales deleted',
            },
        },
        smokescales: {
            name: 'Smoke Scales',
            fields: {
                id: 'ID',
                sex: 'Sex',
                maxv: 'Smoke',
                score: 'Score',
            },
            notifications: {
                created: 'Smoke Scales created |||| %{smart_count} Smoke Scales created',
                updated: 'Smoke Scales updated |||| %{smart_count} Smoke Scales updated',
                deleted: 'Smoke Scales deleted |||| %{smart_count} Smoke Scales deleted',
            },
        },
        commonriskscales: {
            name: 'Common Risk',
            fields: {
                id: 'ID',
                sex: 'Sex',
                age: 'Age',
                avgrisk: 'Avg Risk',
                minrisk: 'Min Risk',
            },
            notifications: {
                created: 'Common Risk Scales created |||| %{smart_count} Common Risk Scales created',
                updated: 'Common Risk Scales updated |||| %{smart_count} Common Risk Scales updated',
                deleted: 'Common Risk Scales deleted |||| %{smart_count} Common Risk Scales deleted',
            },
        },
        indicators: {
            name: 'Indicators',
            fields: {
                id: 'ID',
                name: 'Name',
                parent: 'Parent',
            },
            notifications: {
                created: 'Indicators created |||| %{smart_count} Indicators created',
                updated: 'Indicators updated |||| %{smart_count} Indicators updated',
                deleted: 'Indicators deleted |||| %{smart_count} Indicators deleted',
            },
        },
        singleassesss: {
            name: 'Single Assess',
            fields: {
                id: 'ID',
                assesstype: 'Assess Type',
                assessname: 'Assess Name',
                minv: 'Min Value',
                maxv: 'Max Value',
            },
            notifications: {
                created: 'Single Assess created |||| %{smart_count} Single Assess created',
                updated: 'Single Assess updated |||| %{smart_count} Single Assess updated',
                deleted: 'Single Assess deleted |||| %{smart_count} Single Assess deleted',
            },
        },
        riskanalyses: {
            name: 'Risk Analyses',
            fields: {
                id: 'ID',
                risk: 'Risk',
                hmtype: 'Hmtype',
            },
            notifications: {
                created: 'Risk Analyses created |||| %{smart_count} Risk Analyses created',
                updated: 'Risk Analyses updated |||| %{smart_count} Risk Analyses updated',
                deleted: 'Risk Analyses deleted |||| %{smart_count} Risk Analyses deleted',
            },
        },
        healthintervents: {
            name: 'Health Intervents',
            fields: {
                id: 'ID',
                intervent: 'Intervent',
                hmtype: 'Hmtype',
            },
            notifications: {
                created: 'Health Intervents created |||| %{smart_count} Health Intervents created',
                updated: 'Health Intervents updated |||| %{smart_count} Health Intervents updated',
                deleted: 'Health Intervents deleted |||| %{smart_count} Health Intervents deleted',
            },
        },
        habitassess: {
            name: 'Habits Assess',
            fields: {
                id: 'ID',
                username:'Username',
                name:'Name',
                sex: 'Sex',
                age: 'Age',
                smokeyear: 'Smoke Years',
                drinkyear: 'Drink Years',
                diabetesyear: 'Diabetes Years',
                assess: 'Assess',
                risks: 'Risks',
                intervents: 'Intervents',
            },
            notifications: {    
            },
        },
        bmiassess: {
            name: 'BMI Weight Assess',
            fields: {
                id: 'ID',
                username:'Username',
                name:'Name',
                sex: 'Sex',
                age: 'Age',
                dataset:'bddataset',
                assessresult:'assessresult',
                bmiresult:'bmiresult',
                assess: 'Assess',
                risks: 'Risks',
                intervents: 'Intervents',
            },
            notifications: {    
            },
        },
        bloodpressureassess: {
            name: 'Blood Pressure Assess',
            fields: {
                id: 'ID',
                username:'Username',
                name:'Name',
                sex: 'Sex',
                age: 'Age',
                dataset:'bpdataset',
                assessresult:'assessresult',
                assess: 'Blood Pressure Assess',
                risks: 'Health Risks',
                intervents: 'Health Intervents',
            },
            notifications: {    
            },
        }, 
        bcholesterinassess: {
            name: 'Bcholesterin Assess',
            fields: {
                id: 'ID',
                username:'Username',
                name:'Name',
                sex: 'Sex',
                age: 'Age',
                dataset:'bsdataset',
                assessresult:'assessresult',                
                assess: 'Bcholesterin Assess',
                risks: 'Health Risks',
                intervents: 'Health Intervents',
            },
            notifications: {    
            },
        },
        icvdassess: {
            name: 'ICVD Risk Assess',
            fields: {
                id: 'ID',
                username:'Username',
                name:'Name',
                sex: 'Sex',
                age: 'Age',
                assessresult:'assessresult',                
                assess: 'ICVD Assess',
                risks: 'ICVD Risks',
                intervents: 'Health Intervents',
            },
            notifications: {    
            },
        },        
    },
};

export default customEnglishMessages;
