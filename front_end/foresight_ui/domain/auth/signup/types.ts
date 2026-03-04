

export interface SignUpDTO {
  username: string;
  email: string;
  password: string;
}


export type SignUpResponse = {
  success: boolean;
  user: {
    id: string;
    username: string;
    email: string;
  };
};