export type UserAccountResponse = {
  userAccountId: number;
  name: string;
  username: string;
  about: string;
  categories: string;
  location: string;
  website: string;
  joinedDate: Date;
  birthDate: Date;
  isVerified: boolean;
  isPrivate: boolean;
  isOfficialAccount: boolean;
  email: string;
  phoneNumber: string;
  country: string;
  profilePicture: string;
  userAccountStatistics: UserAccountStatistics;
};

export type UserAccountStatistics = {
  followerCount: number;
  followingCount: number;
};
