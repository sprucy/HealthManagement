import { useMediaQuery, Theme } from "@mui/material";
import { Datagrid, List, NumberField, TextField } from 'react-admin';

export const PermissionList = () => (
    <List>
        <Datagrid>
            <TextField source="id" />
            <TextField source="name" />
            <TextField source="codename" />
        </Datagrid>
    </List>
);

export default PermissionList;