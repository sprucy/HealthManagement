import { useMediaQuery, Theme } from "@mui/material";
import { Datagrid, List, TextField, ReferenceArrayField } from 'react-admin';
import { useTranslate } from 'react-admin';

export const GroupList = () => {
    const translate = useTranslate();
    return(
        <List>
            <Datagrid>
                <TextField source="id" />
                <TextField source="name" />
                <ReferenceArrayField reference="permissions" source="permissions" />
            </Datagrid>
        </List>
    );
};

export default GroupList;