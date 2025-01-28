import { useMediaQuery, Theme } from "@mui/material";
import { useTranslate } from 'react-admin';
import {
    List,
    Datagrid,
    TextField, 
    ReferenceArrayField,
    SearchInput,
    SimpleForm,
  } from "react-admin";

export const GroupShow = () => {
    const translate = useTranslate();
    return(
        <SimpleForm >
            <div >
                <TextField source="id" />
                <TextField source="name" />
                <ReferenceArrayField reference="permissions" source="permissions" label={translate("resources.groups.fields.permissions")} />
            </div>
        </SimpleForm>
    );
};

export default GroupShow;