import { useMediaQuery, Theme } from "@mui/material";
import {
    Edit,
    TextField,
    TextInput,
    DateField,
    DateInput,
    Labeled,
    SelectInput,
    BooleanInput,
    NullableBooleanInput,
    ReferenceField,
    ReferenceArrayInput,
    SelectArrayInput,
    SimpleForm,
    useTranslate,
} from 'react-admin';
import { Card, CardContent, Box, Grid, Typography, Link } from '@mui/material';
import { validateForm } from './UsersCreate';


export const UserEdit = () => {
    const translate = useTranslate();
    const isSmall = useMediaQuery<Theme>((theme) => theme.breakpoints.down("sm"));
    return(
        <Edit title={<UserTitle />} >

            <SimpleForm  validate={validateForm}>
                <div >
                    <Grid container alignItems="center" width={{ xs: '100%', xl: 1200 }} spacing={2}>
                        <Grid item xs={12} md={8}>
                            <Typography variant="h6" gutterBottom>
                                {translate(
                                    'resources.users.fieldGroups.identity'
                                )}
                            </Typography>
                            <Box display={{ xs: 'block', sm: 'flex' }}>
                                <Box flex={1} mr={{ xs: 0, sm: '0.5em' }}>
                                    <TextInput source="username" isRequired />
                                </Box>
                            </Box>
                            <Box display={{ xs: 'block', sm: 'flex' }}>
                                <Box flex={1} mr={{ xs: 0, sm: '0.5em' }}>
                                    <TextInput source="first_name" isRequired />
                                </Box>
                                <Box flex={1} ml={{ xs: 0, sm: '0.5em' }}>
                                    <TextInput source="last_name" isRequired />
                                </Box>
                            </Box>

                            <TextInput type="email" source="email" isRequired />

                            <Box mt="1em" />

                            <Typography variant="h6" gutterBottom>
                                {translate(
                                    'resources.users.fieldGroups.stats'
                                )}
                            </Typography>
                            <Box display={{ xs: 'block', sm: 'flex' }}>
                                <Box flex={1} mr={{ xs: 0, sm: '0.5em' }}>
                                    <BooleanInput
                                                row={true}
                                                source="is_superuser"
                                    />
                                </Box>
                                <Box flex={1} ml={{ xs: 0, sm: '0.5em' }}>
                                    <BooleanInput
                                                row={true}
                                                source="is_staff"
                                    />
                                </Box>
                                <Box flex={1} ml={{ xs: 0, sm: '0.5em' }}>
                                    <BooleanInput
                                                row={true}
                                                source="is_active"
                                    />
                                </Box>
                            </Box>
                            <Box mt="1em" />
                            <Box display={{ xs: 'block', sm: 'flex' }}>
                                {/* <Labeled source="date_joined">
                                    <DateField source="date_joined" showTime />
                                </Labeled>
                                <Labeled source="last_login">
                                    <DateField source="last_login" showTime />
                                </Labeled> */}
                                <Box flex={1} mr={{ xs: 0, sm: '0.5em' }}>
                                    <DateInput source="date_joined" />
                                </Box>
                                <Box flex={1} ml={{ xs: 0, sm: '0.5em' }}>
                                    <DateInput source="last_login" />
                                </Box>
                            </Box>

                            <Box mt="1em" />
                            <Typography variant="h6" gutterBottom>
                                {translate(
                                    'resources.users.fieldGroups.permissions'
                                )}
                            </Typography>                            
                            <Box display={{ xs: 'block', sm: 'flex' }}>
                                <Box flex={1} mr={{ xs: 0, sm: '0.5em' }}>
                                    <ReferenceArrayInput 
                                        reference="groups" 
                                        source="groups" 
                                    >
                                        <SelectArrayInput source="groups" />
                                    </ReferenceArrayInput>
                                </Box>
                                <Box flex={1} ml={{ xs: 0, sm: '0.5em' }}>
                                <ReferenceArrayInput 
                                        reference="permissions" 
                                        source="user_permissions" 
                                    >
                                        <SelectArrayInput />
                                    </ReferenceArrayInput>
                                </Box>
                            </Box>
                        </Grid>
                    </Grid>
                </div>
            </SimpleForm>
        </Edit>
    );
};

const UserTitle = () => (
///    <FullNameField source="last_name" size="32" sx={{ margin: '5px 0' }} />
    <TextField source="last_name">

    </TextField>);

export default UserEdit;

