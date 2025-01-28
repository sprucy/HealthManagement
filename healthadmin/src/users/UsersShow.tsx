import { useMediaQuery, Theme } from "@mui/material";
import { useTranslate } from 'react-admin';
import {

    SimpleShowLayout,
    Show,
    TextField, 
    NumberField,
    BooleanField,
    DateField,
    ImageField,
    EmailField,
    ReferenceField,
    ReferenceArrayField,
    SearchInput,
  } from "react-admin";

export const UserShow = () => {
    const translate = useTranslate();
    return(
        <Show>
        <SimpleShowLayout>
                <TextField source="username" />
                <TextField source="last_name" />
                <TextField source="first_name" />
                <EmailField source="email" />
                <DateField source="last_login" showTime />
                <DateField source="date_joined" />
                <BooleanField source="is_superuser" />
                <BooleanField source="is_staff" />
                <BooleanField source="is_active" />
                <ReferenceArrayField reference="groups" source="groups" label={translate("resources.users.fields.groups")} />
                <TextField source="user_permissions" />
            </SimpleShowLayout>
        </Show>
    );
};

export default UserShow;