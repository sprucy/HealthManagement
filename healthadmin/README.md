# healthadmin

## Installation

Install the application dependencies by running:

```sh
yarn
```

## Development

Start the application in development mode by running:

```sh
yarn dev
```

## Production

Build the application in production mode by running:

```sh
yarn build
```

## DataProvider

The included data provider use [ra-data-simple-rest](https://github.com/marmelab/react-admin/tree/master/packages/ra-data-simple-rest). It fits REST APIs using simple GET parameters for filters and sorting. This is the dialect used for instance in [FakeRest](https://github.com/marmelab/FakeRest).

You'll find an `.env` file at the project root that includes a `VITE_JSON_SERVER_URL` variable. Set it to the URL of your backend.


Faqs:
1. Error: listen EACCES: permission denied 0.0.0.0:5173 异常
    1、先判断是否是端口占用的问题导致的
    netstat -ano| findstr 5173
    发现并没有程序在使用这个端口
    2、改用管理员再运行一遍
    发现仍然不行
    3、使用管理员权限运行以下命令
    net stop winnat
    net start winnat