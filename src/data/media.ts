import data from './media.json';
export type Study = {
  status: 'approved' | 'draft' | 'planned'; statusLabel: string;
  video: string | null; poster: string | null; captions: string | null;
  captionLabel?: string;
  posterAlt?: string; posterLabel?: string; reviewLinkLabel?: string;
  duration: number; model: string | null; resolution: string | null; reviewed: boolean;
  studyLabel: string; caption: string; description: string; watchFor: string; reviewNote: string;
  reviewUrl: string; cast: string[]; coverageScope: string; audioLabel: string;
  related: {label: string; href: string}[];
  archive: {video: string; poster: string; duration: number; reviewNote: string};
};
export const media = data as Record<string, Study>;
