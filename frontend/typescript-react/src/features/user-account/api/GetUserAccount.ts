import { useQuery } from "react-query";
import { axios } from "../../../common/axios";
import { ExtractFnReturnType, QueryConfig } from "../../../common/react-query";
import { UserAccountResponse } from "../types/UserAccountResponse";
// import { UserAccountResponse } from "../types/UserAccountResponse";

export const getUserAccount = ({
  username,
}: {
  username: string;
}): Promise<UserAccountResponse> => {
  return axios.get(`/username/${username}`);
};

type QueryFnType = typeof getUserAccount;

type UseUserAccountOptions = {
  username: string;
  config?: QueryConfig<QueryFnType>;
};

export const useUserAccount = ({ username, config }: UseUserAccountOptions) => {
  return useQuery<ExtractFnReturnType<QueryFnType>>({
    ...config,
    queryKey: ["userAccount", username],
    queryFn: () => getUserAccount({ username }),
  });
};
