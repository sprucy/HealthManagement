import { useMediaQuery, Theme } from "@mui/material";
import { List, SimpleList, Datagrid, TextField, DateField,NumberField,ImageField,BooleanField,EmailField,ReferenceField } from "react-admin";


export const UserinfoList = () => {
    return(
        <List> 
            <Datagrid>
                <ReferenceField source="user" reference="users"  link="show"/>
                <TextField source="ssn" />
                <DateField source="birthday" />
                <TextField source="sex" />
                <TextField source="phone" />
                <TextField source="province" />
                <TextField source="city" />
                <TextField source="org" />
                <TextField source="job" />
                <TextField source="address" />
                <ImageField source="photo" />
            </Datagrid>
        </List>
    );
};