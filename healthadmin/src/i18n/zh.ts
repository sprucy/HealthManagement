import { TranslationMessages } from 'react-admin';
import chineseMessages from '@haxqer/ra-language-chinese';
import englishMessages from 'ra-language-english';

const customChineseMessages: TranslationMessages = {
    ...chineseMessages,
    health: {
        search: '查询',
        configuration: '配置',
        language: '语言',
        theme: {
            name: '主题',
            light: '日间模式',
            dark: '夜间模式',
        },
        systemuserwarning:'系统管理用户,无个人健康信息数据!',
        dashboard: {
            title: '概览',
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
            heightchart:'身高测量图',
            weightchart:'体重测量图',
            bmichart: 'BMI计算图',
            waistchart: '腰围测量图',
            weekweight: '周平均体重',
            weekbmi: '周平均体质系数',
            weekwaist: '周平均腰围',
        },
        bloodpressureassess: {
            charttitle: '血压测量图',
            measuretime: '测量时间',
            dbp: '收缩压',
            sbp: '舒张压',
            hr: '心率',
            avgdbp: '平均收缩压',
            avgsbp: '平均舒张压',
            avghr: '平均心率',
        },        
        bcholesterinassess: {
            charttitle: '血脂测量图',
            measuretime: '测量时间',            
            tc: '总胆固醇',
            ldl: '低密度',
            hdl: '高密度',
            tg: '甘油三酯',            
            avgtc: '平均总胆固醇',
            avgldl: '平均低密度',
            avghdl: '平均高密度',
            avgtg: '平均甘油三酯',
        }, 
        icvdassess:{
            minrisk: '同龄十年最低发病绝对危险度',
            avgrisk: '同龄十年发病平均绝对危险度',
            currisk: '本人评估十年发病绝对危险度',
        }, 
        menu: {
            system: '系统管理',
            data: '健康信息',
            analytic: '健康分析',
            standard: '标准管理',
            evaluate: '健康评估',
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
            name: '用户',
            fields: {
                username: '用户名',
                first_name: '名字',
                last_name: '姓氏',
                email: '邮箱',
                last_login: '登录日期',
                date_joined: '注册日期',
                is_superuser: '超级管理员',
                is_staff: '后台管理',
                is_active: '活动状态',
                groups: '组',
                password: '密码',
                confirm_password: '确认密码',
                user_permissions: '用户权限',
            },
            filters: {
                last_visited: '上次访问',
                today: '今日',
                this_week: '本周',
                last_week: '上周',
                this_month: '本月',
                last_month: '上月',
                earlier: '更早',
                has_ordered: '排序',
                has_newsletter: '新消息',
                group: '组',
            },
            fieldGroups: {
                identity: '标识',
                address: '地址',
                stats: '状态',
                history: '历史记录',
                permissions: '权限',
                password: '密码',
                change_password: '修改密码',
            },
            page: {
                delete: '删除用户',
            },
            errors: {
                password_mismatch:
                    '两次密码输入不同.',
            },
            notifications: {
                created:
                    '建立用户',
                updated:
                    '更新用户',
                deleted:
                    '删除用户',
            },
        },
        groups: {
            name: '组',
            title: '组 %{reference}',
            fields: {
                id: '组ID',
                name: '组名称',
                permissions: '权限',
            },
            notifications: {
                created: '组建立 |||| %{smart_count} 个组建立',
                updated: '组更新 |||| %{smart_count} 个组更新',
                deleted: '组删除 |||| %{smart_count} 个组删除',
            },
        },
        permissions: {
            name: '权限',
            fields: {
                id: '权限ID',
                name: '权限名称',
                codename: '代码名称',
                content_type: '内容类型',
            },
            notifications: {
                created:
                    '权限建立 |||| %{smart_count} 权限建立',
                updated:
                    '权限更新 |||| %{smart_count} 权限更新',
                deleted:
                    '权限删除 |||| %{smart_count} 权限删除',
            },
        },
        userinfos: {
            name: '基本信息',
            fields: {
                user: '用户',
                ssn: '身份证',
                birthday: '生日',
                sex: '性别',
                phone: '电话',
                province: '省份',
                city: '城市',
                org: '单位',
                job: '职位',
                address: '地址',
                photo: '照片',
            },
            notifications: {
                created:
                    '基本信息建立 |||| %{smart_count} 基本信息建立',
                updated:
                    '基本信息更新 |||| %{smart_count} 基本信息更新',
                deleted:
                    '基本信息删除 |||| %{smart_count} 基本信息删除',
            },
        },
        agescales: {
            name: '年龄评估标准',
            fields: {
                id: '标准ID',
                sex: '性别',
                maxv: '最大值',
                score: '分数',
            },
            notifications: {
                created: 'ICVD年龄评估标准建立 |||| %{smart_count} ICVD年龄评估标准建立',
                updated: 'ICVD年龄评估标准更新 |||| %{smart_count} ICVD年龄评估标准更新',
                deleted: 'ICVD年龄评估标准删除 |||| %{smart_count} ICVD年龄评估标准删除',
            },
        },
        bodyinfos: {
            name: '身高体重',
            fields: {
                id: 'ID',
                user: '姓名',
                measuretime: '测量时间',
                height: '身高(cm)',
                weight: '体重(kg)',
                waist: '腰围(cm)',
            },
            notifications: {
                created: '身高体重信息建立 |||| %{smart_count} 身高体重信息建立',
                updated: '身高体重信息更新 |||| %{smart_count} 身高体重信息更新',
                deleted: '身高体重信息删除 |||| %{smart_count} 身高体重信息删除',
            },
        },   
        smokediabetesinfos: {
            name: '吸烟糖尿病史',
            fields: {
                id: 'ID',
                user: '姓名',
                smoke: '吸烟',
                smokestart: '吸烟开始时间',
                drink: '饮酒',
                drinkstart: '饮酒开始时间',
                diabetes: '糖尿病',
                diabetesstart: '糖尿病患病时间',
            },
            notifications: {
                created: '建立吸烟糖尿病史信息 |||| %{smart_count} 建立吸烟糖尿病史信息',
                updated: '更新吸烟糖尿病史信息 |||| %{smart_count} 更新吸烟糖尿病史信息',
                deleted: '删除吸烟糖尿病史信息 |||| %{smart_count} 删除吸烟糖尿病史信息',
            },
        },
        bloodpressures: {
            name: '血压信息',
            fields: {
                id: 'ID',
                user: '姓名',
                measuretime: '测量时间',
                DBP: '舒张压(mmHg)',
                SBP: '收缩压(mmHg)',
                HR: '心率',
            },
            notifications: {
                created: '建立血压信息 |||| %{smart_count} 建立血压信息',
                updated: '更新血压信息 |||| %{smart_count} 更新血压信息',
                deleted: '删除血压信息 |||| %{smart_count} 删除血压信息',
            },
        },
        bcholesterins: {
            name: '血脂信息',
            fields: {
                id: 'ID',
                user: '姓名',
                measuretime: '测量时间',
                TC: '总胆固醇(mmol/L)',
                LDL: '低密度脂蛋白(mmol/L)',
                HDL: '高密度胆固醇(mmol/L)',
                TG: '甘油三酯(mmol/L)',
            },
            notifications: {
                created: '建立血脂信息 |||| %{smart_count} 建立血脂信息',
                updated: '更新血脂信息 |||| %{smart_count} 更新血脂信息',
                deleted: '删除血脂信息 |||| %{smart_count} 删除血脂信息',
            },
        },
        bmiscales: {
            name: 'BMI评估标准',
            fields: {
                id: 'ID',
                bmi: 'BMI',
                wtype: 'Wtype',
            },
            notifications: {
                created: 'BMI评估标准建立 |||| %{smart_count} BMI评估标准建立',
                updated: 'BMI评估标准更新 |||| %{smart_count} BMI评估标准更新',
                deleted: 'BMI评估标准删除 |||| %{smart_count} BMI评估标准删除',
            },
        },
        diabetesscales: {
            name: '糖尿病评估标准',
            fields: {
                id: 'ID',
                sex: '性别',
                diabetes: '是否糖尿病',
                score: '分数',
            },
            notifications: {
                created: 'ICVD糖尿病评估标准建立 |||| %{smart_count} ICVD糖尿病评估标准建立',
                updated: 'ICVD糖尿病评估标准更新 |||| %{smart_count} ICVD糖尿病评估标准更新',
                deleted: 'ICVD糖尿病评估标准删除 |||| %{smart_count} ICVD糖尿病评估标准删除',
            },
        },
        riskevaluatscales: {
            name: '评估风险标准',
            fields: {
                id: 'ID',
                sex: '性别',
                score: '分数',
                risk: '风险值%',
            },
            notifications: {
                created: 'ICVD十年发病风险评估标准建立 |||| %{smart_count} ICVD十年发病风险评估标准建立',
                updated: 'ICVD十年发病风险评估标准更新 |||| %{smart_count} ICVD十年发病风险评估标准更新',
                deleted: 'ICVD十年发病风险评估标准删除 |||| %{smart_count} ICVD十年发病风险评估标准删除',
            },
        },
        weightscales: {
            name: '体重评估标准',
            fields: {
                id: 'ID',
                sex: '性别',
                maxv: '最大值',
                score: '分数',
            },
            notifications: {
                created: 'ICVD体重评估标准建立 |||| %{smart_count} ICVD体重评估标准建立',
                updated: 'ICVD体重评估标准更新 |||| %{smart_count} ICVD体重评估标准更新',
                deleted: 'ICVD体重评估标准删除 |||| %{smart_count} ICVD体重评估标准删除',
            },
        },
        bloodpressurescales: {
            name: '血压评估标准',
            fields: {
                id: 'ID',
                sex: '性别',
                maxv: '收缩压最大值',
                score: '分数',
            },
            notifications: {
                created: 'ICVD血压评估标准建立 |||| %{smart_count} ICVD血压评估标准建立',
                updated: 'ICVD血压评估标准更新 |||| %{smart_count} ICVD血压评估标准更新',
                deleted: 'ICVD血压评估标准删除 |||| %{smart_count} ICVD血压评估标准删除',
            },
        },
        tcscales: {
            name: '血脂评估标准',
            fields: {
                id: 'ID',
                sex: '性别',
                maxv: '总胆固醇最大值',
                score: '分数',
            },
            notifications: {
                created: 'ICVD血脂评估标准建立 |||| %{smart_count} ICVD血脂评估标准建立',
                updated: 'ICVD血脂评估标准更新 |||| %{smart_count} ICVD血脂评估标准更新',
                deleted: 'ICVD血脂评估标准删除 |||| %{smart_count} ICVD血脂评估标准删除',
            },
        },
        smokescales: {
            name: '吸烟评估标准',
            fields: {
                id: 'ID',
                sex: '性别',
                maxv: '是否吸烟',
                score: '分数',
            },
            notifications: {
                created: 'ICVD吸烟评估标准建立 |||| %{smart_count} ICVD吸烟评估标准建立',
                updated: 'ICVD吸烟评估标准更新 |||| %{smart_count} ICVD吸烟评估标准更新',
                deleted: 'ICVD吸烟评估标准删除 |||| %{smart_count} ICVD吸烟评估标准删除',
            },
        },
        commonriskscales: {
            name: '常规风险标准',
            fields: {
                id: 'ID',
                sex: '性别',
                age: '年龄',
                avgrisk: '平均风险%',
                minrisk: '最小风险%',
            },
            notifications: {
                created: 'ICVD十年发病常规风险标准数据建立 |||| %{smart_count} ICVD十年发病常规风险标准数据建立',
                updated: 'ICVD十年发病常规风险标准数据更新 |||| %{smart_count} ICVD十年发病常规风险标准数据更新',
                deleted: 'ICVD十年发病常规风险标准数据删除 |||| %{smart_count} ICVD十年发病常规风险标准数据删除',
            },
        },
        indicators: {
            name: '健康指标分类',
            fields: {
                id: '指标ID',
                name: '指标名称',
                parent: '上级分类',
            },
            notifications: {
                created: '健康指标分类建立 |||| %{smart_count} 健康指标分类建立',
                updated: '健康指标分类更新 |||| %{smart_count} 健康指标分类更新',
                deleted: '健康指标分类删除 |||| %{smart_count} 健康指标分类删除',
            },
        },
        singleassesss: {
            name: '单项评估标准',
            fields: {
                id: 'ID',
                assesstype: '评估类型',
                assessname: '评估指标',
                minv: '最小值',
                maxv: '最大值',
            },
            notifications: {
                created: '单项评估标准建立 |||| %{smart_count} 单项评估标准建立',
                updated: '单项评估标准更新 |||| %{smart_count} 单项评估标准更新',
                deleted: '单项评估标准删除 |||| %{smart_count} 单项评估标准删除',
            },
        },
        riskanalyses: {
            name: '健康风险分析',
            fields: {
                id: 'ID',
                risk: '风险',
                hmtype: '风险类别',
            },
            notifications: {
                created: '健康风险分析数据建立 |||| %{smart_count} 健康风险分析数据建立',
                updated: '健康风险分析数据更新 |||| %{smart_count} 健康风险分析数据更新',
                deleted: '健康风险分析数据删除 |||| %{smart_count} 健康风险分析数据删除',
            },
        },
        healthintervents: {
            name: '健康干预建议',
            fields: {
                id: 'ID',
                intervent: '干预建议',
                hmtype: '风险类别',
            },
            notifications: {
                created: '健康干预建议数据建立 |||| %{smart_count} 健康干预建议数据建立',
                updated: '健康干预建议数据更新 |||| %{smart_count} 健康干预建议数据更新',
                deleted: '健康干预建议数据删除 |||| %{smart_count} 健康干预建议数据删除',
            },
        },
        habitassess: {
            name: '日常习惯评估',
            fields: {
                id: 'ID',
                username:'用户名',
                name:'姓名',
                sex: '性别',
                age: '年龄',
                smokeyear: '吸烟年限',
                drinkyear: '饮酒年限',
                diabetesyear: '糖尿病年限',
                assess: '日常习惯评估',
                risks: '健康风险分析',
                intervents: '健康指导建议',
            },
            notifications: {    
            },
        },
        bmiassess: {
            name: 'BMI体重评估',
            fields: {
                id: 'ID',
                username:'用户名',
                name:'姓名',
                sex: '性别',
                age: '年龄',
                dataset:'bddataset',
                assessresult:'assessresult',
                bmiresult:'bmiresult',
                assess: 'BMI体重评估',
                risks: '健康风险分析',
                intervents: '健康指导建议',
            },
            notifications: {    
            },
        },
        bloodpressureassess: {
            name: '血压评估',
            fields: {
                id: 'ID',
                username:'用户名',
                name:'姓名',
                sex: '性别',
                age: '年龄',
                dataset:'bpdataset',
                assessresult:'assessresult',
                assess: '血压评估',
                risks: '健康风险分析',
                intervents: '健康指导建议',
            },
            notifications: {    
            },
        }, 
        bcholesterinassess: {
            name: '血脂评估',
            fields: {
                id: 'ID',
                username:'用户名',
                name:'姓名',
                sex: '性别',
                age: '年龄',
                dataset:'bsdataset',
                assessresult:'assessresult',                
                assess: '血脂评估',
                risks: '健康风险分析',
                intervents: '健康指导建议',
            },
            notifications: {    
            },
        },               
        icvdassess: {
            name: '缺血性心血管病风险评估',
            fields: {
                id: 'ID',
                username:'用户名',
                name:'姓名',
                sex: '性别',
                age: '年龄',
                assessresult:'assessresult',                
                assess: '血脂评估',
                risks: '健康风险分析',
                intervents: '健康指导建议',
            },
            notifications: {    
            },
        }, 
    },
};

export default customChineseMessages;
