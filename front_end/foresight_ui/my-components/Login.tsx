import { Field } from '@base-ui/react/field';
import { Form } from '@base-ui/react/form';
import { User } from 'lucide-react';
import MyButton from './MyButton';
import Image from 'next/image'; 
import logo from '../../public/logo.png';

const Login = () => {
  return (
    <div className="bg-background-layer-1 p-4 rounded-lg shadow-raised">
      <Image src={logo} alt="Foresight Logo" width={150} height={100} className="mb-4 mx-auto"/>
  
      <Field.Root className='flex flex-col gap-2'>
        <Field.Label className='text-foreground font-medium'>
          Username
        </Field.Label>
        
        <div className="relative">
            <div  className='flex items-center gap-2 bg-background shadow-inset rounded-lg'>
                <User className=' absolute left-3 top-1/2 -translate-y-1/2 text-foreground/50'/>
                <Field.Control className='w-full pl-10 p-3 border border-foreground/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/50' placeholder='Enter your username' />
            </div>
        </div>
        
        <Field.Error className='text-danger/70 text-sm'>
          Please enter your username.
        </Field.Error>
        
        <Field.Description className='text-info/70 text-sm'>
          Login to your account
        </Field.Description>
      </Field.Root>
      <MyButton name='Submit' text='text-success' color='from-success/5 to-success/25' rounded="rounded-xl" icon={null}></MyButton>
    </div>
  );
}

export default Login;