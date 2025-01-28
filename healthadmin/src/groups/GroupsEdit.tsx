import { useMediaQuery, Theme } from "@mui/material";
import {
    Edit,
    TextField,
    TextInput,
    Labeled,
    SelectArrayInput,
    ReferenceArrayInput,
    SimpleForm,
    useTranslate,
} from 'react-admin';
import { Card, CardContent, Box, Grid, Typography, Link } from '@mui/material';



export const GroupEdit = () => {
    const translate = useTranslate();
    return(
        <Edit title={<GroupTitle />} >
            <SimpleForm >
                <div >
                    <Grid container alignItems="center" width={{ xs: '100%', xl: 1200 }} spacing={2}>
                        <Grid item xs={12} md={8}>
                            <Box display={{ xs: 'block', sm: 'flex' }}>
                                <Box flex={1} mr={{ xs: 0, sm: '0.5em' }}>
                                    <TextInput source="id" isRequired />
                                </Box>
                            </Box>
                            <Box display={{ xs: 'block', sm: 'flex' }}>
                                <Box flex={1} mr={{ xs: 0, sm: '0.5em' }}>
                                    <TextInput source="name" isRequired />
                                </Box>
                            </Box>

                            <Box mt="1em" />
                           
                            <Box display={{ xs: 'block', sm: 'flex' }}>
                                <Box flex={1} mr={{ xs: 0, sm: '0.5em' }}>
                                    <ReferenceArrayInput 
                                        reference="permissions" 
                                        source="permissions" 
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

const GroupTitle = () => (
    <TextField source="name">
    </TextField>);

export default GroupEdit;

