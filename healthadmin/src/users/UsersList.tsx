import { useMediaQuery, Theme } from "@mui/material";
import { useTranslate } from 'react-admin';
import {
    List,
    SimpleList,
    Datagrid,
    TextField, 
    NumberField,
    BooleanField,
    DateField,
    ImageField,
    EmailField,
    ReferenceField,
    ReferenceManyField,
    ReferenceArrayField,
    ReferenceManyCount,
    ChipField,
    SingleFieldList,
    CreateButton,
    SearchInput,
    SelectColumnsButton,
    ExportButton,
    TopToolbar,
  } from "react-admin";

const UserListActions = () => (
    <TopToolbar>
        <CreateButton />
        <SelectColumnsButton />
        <ExportButton />
    </TopToolbar>
);

export const UserList = () => {
    const isSmall = useMediaQuery<Theme>((theme) => theme.breakpoints.down("sm"));
    const translate = useTranslate();
    return(
        <List 
            sort={{ field: "last_name", order: "ASC" }}
            filters={[<SearchInput source="q" alwaysOn />]}
            actions={<UserListActions />}
            perPage={25}
        >
            {isSmall ? (
                <SimpleList
                    primaryText={(record) => record.id}
                    secondaryText={(record) => record.username}
                    tertiaryText={(record) => record.email}
                />
            ) : (
                <Datagrid>
                    <TextField source="username" />
                    <TextField source="last_name" />
                    <TextField source="first_name" />
                    <EmailField source="email" />
                    <DateField source="last_login" showTime />
                    <DateField source="date_joined" />
                    <BooleanField source="is_superuser" />
                    <BooleanField source="is_staff" />
                    <BooleanField source="is_active" />
                    <ReferenceArrayField reference="groups" source="groups" />
                    <ReferenceArrayField reference="permissions" source="user_permissions" />
                </Datagrid>
            )}
        </List>
    );
};

export default UserList;