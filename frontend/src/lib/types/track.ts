import type Services from "$lib/enums/services";
import type User from "./user";

export default interface Track {
	id: number;
	song_id: string;
	service: Services;
	added_by_user: number;
	title: string;
	artist: string;
	cover: string;
	added_by: User;
};
